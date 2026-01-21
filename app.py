import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="The Cutting Edge", page_icon="🌱", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #2d5a27 0%, #4a9c3d 50%, #3d8a35 100%); }
    .main-header { text-align: center; color: white; padding: 20px 0; }
    .main-header h1 { color: #fffef5; font-size: 2.5rem; margin-bottom: 0; }
    .main-header .highlight { color: #f5a623; }
    .card { background: #fffef5; border-radius: 20px; padding: 25px; margin: 15px 0; border-top: 6px solid #4a9c3d; }
    .category-badge { background: #4a9c3d; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 15px; }
    .surface-text { color: #666; font-style: italic; padding: 10px 0; border-bottom: 2px dashed #ddd; margin-bottom: 15px; }
    .reason-label { color: #f5a623; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
    .reason-text { color: #2d5a27; font-size: 1.3rem; font-weight: bold; line-height: 1.4; }
    .approach-label { color: #4a9c3d; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
    .approach-text { color: #2d5a27; font-size: 1.1rem; line-height: 1.6; }
    .success-box { background: #d4edda; border-radius: 10px; padding: 15px; text-align: center; color: #2d5a27; font-weight: bold; }
    .guide-output { background: linear-gradient(135deg, #e8f5e6, #d4edda); border-radius: 15px; padding: 20px; margin-top: 20px; border-left: 5px solid #4a9c3d; }
    .guide-section { margin-bottom: 15px; }
    .guide-label { color: #4a9c3d; font-weight: bold; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 5px; }
    .guide-text { color: #2d5a27; font-size: 1.1rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

objections = [
    {"id": 1, "category": "Commitment", "surface": "I only need a one-time service", "reason": "They don't want to be locked into a rigid schedule", "rebuttal": "The three cuts are completely flexible — use them whenever you need, no set schedule required. Life happens, and we work around it."},
    {"id": 2, "category": "Commitment", "surface": "I only need a one-time service", "reason": "They're worried about paying upfront for services they might not use", "rebuttal": "No upfront payment ever. You're only charged three days after each service is completed. You're never paying for something you haven't received yet."},
    {"id": 4, "category": "Commitment", "surface": "I only need a one-time service", "reason": "They're testing the waters and don't trust committing to a new company", "rebuttal": "That's exactly why we have the three-day quality window — you see the work, inspect it, and we fix any mistakes BEFORE payment. It's basically a trial run with zero risk."},
    {"id": 5, "category": "Timing", "surface": "I need someone to come out today", "reason": "They have a genuine urgent situation (event, guests coming, etc.)", "rebuttal": "After signup, you can message your crew directly through the app and ask if they can fit you in sooner. No guarantees, but it's worth a shot and crews often accommodate when they can."},
    {"id": 6, "category": "Timing", "surface": "I got an HOA notice and need it done ASAP", "reason": "They're stressed about a violation or fine deadline", "rebuttal": "I totally understand the pressure. While we do have a 48-hour turnaround, we can send you an email confirmation right after signup that you can forward to your HOA to show you have service scheduled. That usually buys you the time you need."},
    {"id": 7, "category": "Timing", "surface": "I need someone to come out today", "reason": "They're impatient and think all companies take forever", "rebuttal": "We have the fastest turnaround in the industry — 48 hours for first service. We price your yard before we show up, so there's no waiting around for quotes. Most competitors can't touch that speed."},
    {"id": 8, "category": "Timing", "surface": "48 hours is too long to wait", "reason": "They're comparing to a neighbor kid who can come over anytime", "rebuttal": "With us you get insured professionals, guaranteed quality, and a team to back it up if anything goes wrong. That 48 hours gets you reliability you can count on every time."},
    {"id": 9, "category": "Timing", "surface": "I'll just call back when I actually need it", "reason": "They don't want to plan ahead or commit to anything now", "rebuttal": "Totally fine — but keep in mind there's still a 48-hour window when you do call. If you grab a spot now, you lock in availability and can cancel free up to 48 hours before if plans change."},
    {"id": 10, "category": "Price", "surface": "Your prices are too high", "reason": "They're comparing to the cheapest option they can find", "rebuttal": "Every pro is verified and insured, so you're not gambling on some random person. You're paying for peace of mind and consistency, not just a mow."},
    {"id": 11, "category": "Price", "surface": "Your prices are too high", "reason": "They've been burned before paying good money for bad service", "rebuttal": "You have a full three days after service to inspect everything before you're charged. See an issue? Let us know and we send someone to fix it. We have a whole team dedicated to making it right."},
    {"id": 12, "category": "Price", "surface": "Your prices are too high", "reason": "They don't understand what's included in the service", "rebuttal": "That price covers the full service plus our quality guarantee, insurance, and support team. What specifically were you hoping to get done? Let me make sure we're comparing apples to apples."},
    {"id": 13, "category": "Price", "surface": "I found someone cheaper", "reason": "They're price-focused but haven't thought about risk", "rebuttal": "Are they insured? What happens if they damage something or don't show up? With us, you're protected — and you don't pay until three days after service when you've confirmed you're happy."},
    {"id": 14, "category": "Shopping Around", "surface": "I'm getting other quotes first", "reason": "They already have a quote from another company but something's off about it", "rebuttal": "What's giving you hesitation with them? (Let them talk — then position how we compare on whatever concern they raise.)"},
    {"id": 15, "category": "Shopping Around", "surface": "I'm not ready to commit yet", "reason": "They haven't actually gotten other quotes, just stalling", "rebuttal": "Is there something specific holding you back? (Probe for the real objection — it's usually price, trust, or timing. Then address that directly.)"},
    {"id": 16, "category": "Shopping Around", "surface": "I want to think about it", "reason": "They're interested but genuinely need time to decide", "rebuttal": "Totally fair. Want me to save a spot on the schedule for you? No charge until after service, and you can cancel up to 48 hours before if you change your mind or find someone else."},
    {"id": 17, "category": "Shopping Around", "surface": "I need to talk to my spouse first", "reason": "They actually do need to check with someone else", "rebuttal": "Of course! I can hold a spot for you so you don't lose availability. No charge until after service, and you can cancel anytime up to 48 hours before. Want me to lock that in while you chat with them?"},
    {"id": 18, "category": "Shopping Around", "surface": "I need to talk to my spouse first", "reason": "They're using it as an excuse to get off the phone", "rebuttal": "Absolutely, I get it. Is there anything I can answer right now that might help that conversation? (Probe gently — often there's a real objection hiding underneath.)"},
    {"id": 19, "category": "Payment", "surface": "Can I pay with cash?", "reason": "They don't like having cards on file with companies", "rebuttal": "Card-only actually protects you — your bank has your back if anything ever goes wrong. It's an extra layer of security you don't get with cash."},
    {"id": 20, "category": "Payment", "surface": "Can I pay with cash?", "reason": "They just prefer cash transactions in general", "rebuttal": "It's actually a benefit for everyone — crews know they're guaranteed payment, which means they show up motivated and ready to do great work. Protects you and them."},
    {"id": 21, "category": "Payment", "surface": "I don't want my card charged automatically", "reason": "They're worried about unauthorized or surprise charges", "rebuttal": "You won't be charged until three days after service — and only after you've had time to inspect the work. If there's any issue, you contact us before that window closes and we make it right first."},
    {"id": 22, "category": "Fees", "surface": "What's this long grass fee?", "reason": "They're worried about surprise charges after the fact", "rebuttal": "We mention it upfront specifically so there are no surprises. If your grass is under 9 inches, it won't apply. We're just being transparent in case it's relevant to your yard."},
    {"id": 23, "category": "Fees", "surface": "That long grass fee seems unfair", "reason": "They think it's just a way to upcharge them", "rebuttal": "It's actually industry standard — overgrown yards take significantly more time and wear on equipment. We keep it fair: only applies at 9 inches or above, and we're telling you NOW so there are no surprises."},
    {"id": 24, "category": "Trust", "surface": "I've never heard of your company", "reason": "They're skeptical of trying something new", "rebuttal": "That's fair — if you Google us, you'll see we have amazing reviews. And because you don't pay until three days after service, you can see the quality for yourself before any money changes hands."},
    {"id": 25, "category": "Trust", "surface": "How do I know the crew will do a good job?", "reason": "They've had bad experiences with lawn services before", "rebuttal": "Every pro is insured and vetted. Plus you have three full days to inspect before you're charged. If anything's off, our quality team fixes it — that's literally their whole job."},
    {"id": 26, "category": "Trust", "surface": "What if I don't like the service?", "reason": "They want to know there's a safety net", "rebuttal": "You have a three-day window after service to review everything before you're charged. If something's not right, reach out and we'll send someone to correct it. You're never stuck paying for work you're not happy with."}
]

dispositions = ["Already Hired A Provider", "Arrival Time", "Broken Address", "Callback", "Dead Air", "Disconnected", "Drop Voicemail", "Duplicate", "Frequency Minimum", "Insufficient Capacity", "Junk Contact", "Less Than 48 Hour Turn-Around", "LGF - Long Grass Fee", "Minimum Cuts Requirement", "No In-Person Quote", "Not DM", "Timing - Unable to Qualify", "Not Qualified - Refuse Contact", "Not Qualified - Telemarketer", "Order Complexity", "Out Of Area", "Oversized Lot", "Pre Paid Card", "Price", "Property Manager", "Provider Inquiry", "Rejected CC", "Rejected CC - Online Signup", "Rejected Subcontracting", "Services Not Offered", "Support Call", "Next Spring", "Test"]

guide_scenarios = {
    "One-Time Service": {
        "openings": {
            "Empathetic": "I totally hear you — a lot of people start out thinking they just need a one-time cleanup.",
            "Curious": "Got it! Can I ask what's prompting the need right now? Just trying to get a sense of what you're dealing with.",
            "Direct": "Here's the good news — we actually make it super flexible for exactly that reason."
        },
        "points": {
            "Flexible scheduling": "You can use your three cuts whenever you want — no set schedule, no pressure. Life happens, and we work around it.",
            "No upfront payment": "You never pay upfront. We only charge three days after each service is done, so you see the work first.",
            "Pro learns your lawn": "When the same pro comes back, they get to know your lawn and your preferences. Better results every time.",
            "3-day quality window": "If anything's not right, you have three full days to let us know and we'll fix it before you're ever charged.",
            "Cancel anytime": "You can cancel up to 48 hours before any scheduled service — no fees, no hassle."
        },
        "closes": {
            "Soft": "Would it help if I saved you a spot on the schedule? No commitment until after the service is done.",
            "Assumptive": "Let's go ahead and get you set up — what address are we working with?",
            "Question": "What's the main thing still holding you back?"
        }
    },
    "Price Concern": {
        "openings": {
            "Empathetic": "I completely understand — price is always a factor, and I want to make sure you're getting real value.",
            "Curious": "Totally fair. When you say the price feels high, are you comparing to another quote or just what you expected?",
            "Direct": "Let me tell you exactly what you're getting for that price, because I think it's actually a great deal."
        },
        "points": {
            "Insured professionals": "Every pro on our platform is verified and insured. You're not gambling on some random person showing up.",
            "Quality guarantee": "You have a full three days to inspect the work before you're charged. If anything's off, we fix it first.",
            "Dedicated support team": "We have a whole team whose only job is making sure you're happy with the service.",
            "No surprise charges": "The price you see is the price you pay — we're upfront about everything, including any potential fees.",
            "Compare apples to apples": "Make sure you're comparing the full package — insurance, support, and our quality guarantee included."
        },
        "closes": {
            "Soft": "How about this — let's get you on the schedule and you can see the quality for yourself. You won't pay until three days after.",
            "Assumptive": "I think once you see the quality, the price will make total sense. Let's get you on the schedule.",
            "Question": "If the quality matches what I'm telling you, would that price feel fair?"
        }
    },
    "Timing / Need It Today": {
        "openings": {
            "Empathetic": "I totally get it — when you need it done, you need it done. Let me see what we can do.",
            "Curious": "Sounds urgent! What's going on — got an event coming up or just hit that breaking point with the yard?",
            "Direct": "So here's the deal — we have a 48-hour turnaround, but let me tell you why that's actually still the fastest around."
        },
        "points": {
            "Fastest in industry": "48 hours is actually the fastest turnaround in the industry. We price before we arrive, so there's no waiting around.",
            "Message your crew": "After signup, you can message your crew directly through the app and ask if they can squeeze you in sooner. Worth a shot!",
            "HOA email": "If you've got an HOA breathing down your neck, we can send you a confirmation email right away that you can forward to them.",
            "Lock in your spot": "If you grab a spot now, you're guaranteed on the schedule. Wait, and availability might fill up.",
            "Free cancellation": "You can cancel up to 48 hours before if your situation changes — no penalty."
        },
        "closes": {
            "Soft": "Want me to lock in the earliest available slot? You can always message the crew to see if they can come sooner.",
            "Assumptive": "Let's get you scheduled for the first available — what's the address?",
            "Question": "If we can get you in within 48 hours, does that work for your timeline?"
        }
    },
    "Shopping Around": {
        "openings": {
            "Empathetic": "That makes total sense — it's smart to know your options before deciding.",
            "Curious": "Totally fair! Have you already talked to other companies, or are you just starting to look around?",
            "Direct": "I'd love the chance to show you why we stand out. Can I ask what's most important to you in a lawn service?"
        },
        "points": {
            "Compare protection": "Make sure whoever you go with is insured. If they damage something or don't show, you want to be covered.",
            "Our reviews": "If you Google us, you'll see we have amazing reviews. People love working with us.",
            "No risk to try": "You don't pay until three days after service, so you can literally see the quality before any money changes hands.",
            "Hold your spot": "I can save a spot on the schedule for you while you decide — no commitment, no charge until after service.",
            "Easy cancellation": "Even after you book, you can cancel up to 48 hours before if you find someone else. Zero pressure."
        },
        "closes": {
            "Soft": "How about I hold a spot for you? No commitment — just keeps your options open while you decide.",
            "Assumptive": "Let's get you on the schedule. If you find someone better, you can cancel anytime before 48 hours out.",
            "Question": "What would you need to see from us to feel confident going with us over someone else?"
        }
    },
    "Payment Method": {
        "openings": {
            "Empathetic": "I get it — a lot of people ask about that. Let me explain why we do it this way.",
            "Curious": "Totally fair question! Is there a specific concern with using a card, or is it just preference?",
            "Direct": "We only accept major credit or debit cards, but here's why that's actually a good thing for you."
        },
        "points": {
            "Bank protection": "With a card, your bank has your back. If anything ever went wrong, you've got that extra layer of protection.",
            "Crews get paid": "It also means our crews know they're guaranteed payment, so they show up ready to do great work.",
            "No upfront charge": "Remember, we don't charge until three days after the service — so your card isn't hit until you've seen the work.",
            "Secure system": "Your card info is stored securely. We take that seriously.",
            "Industry standard": "Most professional services work this way now. It protects everyone involved."
        },
        "closes": {
            "Soft": "Does that make sense? I promise it's set up to protect you, not complicate things.",
            "Assumptive": "Let's get you set up — I just need a card on file and we're good to go.",
            "Question": "If you knew you wouldn't be charged until three days after and could dispute anything with your bank, would that feel okay?"
        }
    },
    "Fees (Long Grass Fee)": {
        "openings": {
            "Empathetic": "I totally get the concern — nobody likes surprise fees. Let me explain exactly how this works.",
            "Curious": "Great question! Do you have a sense of how tall your grass is right now?",
            "Direct": "So I want to be upfront with you about this — that's actually why I'm mentioning it now."
        },
        "points": {
            "Transparency": "We're telling you NOW so there are no surprises later. That's the whole reason we bring it up.",
            "Industry standard": "This is actually standard across the industry — overgrown yards take more time and wear on equipment.",
            "9 inch threshold": "It only applies if the grass is 9 inches or taller. If your lawn is maintained, it won't apply at all.",
            "Up to 100% of base": "If it does apply, it can be up to 100% of your base mowing price — but only when it's really overgrown.",
            "One-time situation": "Usually this only comes up on the first cut if it's been a while. After that, regular service keeps it under control."
        },
        "closes": {
            "Soft": "Does that make sense? We just want to be transparent so you know exactly what to expect.",
            "Assumptive": "Now that you know how it works, let's get you on the schedule. What's the address?",
            "Question": "Does your lawn sound like it might be in that range, or do you think you're under 9 inches?"
        }
    },
    "Trust / Never Heard of You": {
        "openings": {
            "Empathetic": "That's totally fair — I'd want to know who I'm working with too.",
            "Curious": "Totally understand! What would help you feel more comfortable giving us a shot?",
            "Direct": "Let me tell you a bit about us and why so many people trust us with their lawns."
        },
        "points": {
            "Amazing reviews": "If you Google us, you'll see we have amazing reviews. Real people, real experiences.",
            "All pros insured": "Every single pro on our platform is verified and insured. We don't let just anyone on here.",
            "Quality guarantee": "You have three full days after service to inspect the work before you're charged.",
            "Dedicated quality team": "We have a whole team whose only job is making things right if anything's ever off.",
            "No payment until satisfied": "You don't pay until three days after the service, so you see the quality before any money changes hands.",
            "Fix before you pay": "If there's any issue, we send someone to fix it BEFORE you're ever charged."
        },
        "closes": {
            "Soft": "How about you check out our reviews and let me save you a spot in the meantime? No pressure.",
            "Assumptive": "I think once you see the quality, you'll be glad you went with us. Let's get you scheduled.",
            "Question": "What would make you feel confident enough to give us a shot?"
        }
    }
}

attach_guides = {
    "Lawn Treatment": {
        "triggers": ["Weeds everywhere", "Grass is turning brown", "Neighbor's lawn looks better", "Lawn looks thin/patchy", "Weeds keep coming back", "Yellow spots"],
        "openings": {
            "Empathetic": "I hear that a lot — dealing with weeds and patchy grass can be really frustrating, especially when you feel like you've tried everything.",
            "Curious": "Have you noticed if it's more weeds, or is the grass itself looking thin and unhealthy? Just trying to get a picture of what you're dealing with.",
            "Direct": "Sounds like your lawn could really benefit from our lawn treatment program — let me tell you what it includes."
        },
        "points": {
            "Fertilizer for green-up": "It includes fertilizer that helps thicken up your grass and get that green color back.",
            "Pre-emergent stops new weeds": "There's a pre-emergent that stops weeds before they even start — so you're not constantly fighting new ones.",
            "Post-emergent kills existing weeds": "It also has post-emergent to knock out the weeds that are already there.",
            "Results in weeks": "Most people see a real difference within just a few weeks.",
            "Pro learns your lawn": "And since the same pro comes back, they get to know your lawn and what it needs over time."
        },
        "closes": {
            "Soft": "Want me to add that on so we can start getting your lawn back in shape?",
            "Assumptive": "Let's go ahead and add the lawn treatment — that way we're tackling the root of the problem, not just mowing over it.",
            "Question": "Would it help to get the lawn treatment started at the same time so you're not dealing with two separate things?"
        },
        "pro_tip": "If they mention weeds, ask if they've noticed them in specific areas or all over. This helps you explain how the pre-emergent prevents new ones while post-emergent handles what's already there."
    },
    "Leaf Removal": {
        "triggers": ["Leaves are piling up", "Yard is covered in leaves", "Can't even see my grass", "Fall cleanup", "Leaves are out of control"],
        "openings": {
            "Empathetic": "Yeah, this time of year it feels like you clean them up and they're right back the next day. It's a lot to keep up with.",
            "Curious": "How bad has it gotten? Are we talking a light layer or is the grass completely buried at this point?",
            "Direct": "We actually offer leaf removal too — and it's worth doing sooner rather than later."
        },
        "points": {
            "Protects your lawn": "Leaves left too long can actually suffocate your grass and cause dead patches underneath.",
            "Instant curb appeal": "Once they're cleared out, your whole yard looks cleaner and more cared for right away.",
            "Saves you time": "It's one of those jobs that takes forever to do yourself but our crew can knock it out quickly.",
            "Prevents mold and pests": "Wet leaves can also lead to mold and attract pests, so it's good to get ahead of it.",
            "One crew handles it": "We can do it the same time as your mow so you're not scheduling multiple visits."
        },
        "closes": {
            "Soft": "Want me to add leaf removal to this visit so we can get that taken care of for you?",
            "Assumptive": "Let's add the leaf removal too — no point mowing over leaves, and it'll protect your grass going into winter.",
            "Question": "Would it be easier if we just handled the leaves while we're already there?"
        },
        "pro_tip": "Mention the lawn health angle — most people don't realize leaves can actually damage grass if left too long. It turns the conversation from 'extra service' to 'protecting your lawn.'"
    },
    "Bush Trimming": {
        "triggers": ["Bushes are overgrown", "Shrubs are out of control", "Everything looks messy", "Curb appeal", "Getting ready to sell", "HOA notice about bushes"],
        "openings": {
            "Empathetic": "Overgrown bushes can really make the whole yard feel messy, even when the lawn itself looks good. I totally get it.",
            "Curious": "How long has it been since they were last trimmed? Sometimes they just need a good reset to look sharp again.",
            "Direct": "We do bush trimming too, and honestly it's one of the fastest ways to boost your curb appeal."
        },
        "points": {
            "Instant curb appeal": "Trimmed bushes make a huge difference in how the whole property looks from the street.",
            "Keeps bushes healthy": "Regular trimming actually keeps them healthier and growing the right way.",
            "HOA compliant": "If you've got an HOA, this keeps you in compliance so you don't have to worry about notices.",
            "Frames the home nicely": "Well-maintained bushes frame your home and make everything look more polished.",
            "Same visit convenience": "We can do it during the same visit as your mow, so it's one less thing to coordinate."
        },
        "closes": {
            "Soft": "Want me to add bush trimming so we can get everything looking sharp at once?",
            "Assumptive": "Let's add the bush trimming — it'll really complete the look and you won't have to think about it.",
            "Question": "Would it help to have us handle the bushes while we're already out there?"
        },
        "pro_tip": "If they mention selling their home or HOA issues, lean into urgency — trimmed bushes are one of the fastest ways to boost curb appeal, and it's often the first thing buyers and HOAs notice."
    },
    "Flower Bed Weeding": {
        "triggers": ["Flower beds are a mess", "Weeds in my beds", "Can't even see my flowers", "Landscaping looks rough", "Beds are overgrown"],
        "openings": {
            "Empathetic": "Flower beds can get out of hand so fast — one week they're fine, the next week weeds have taken over. It's a lot to maintain.",
            "Curious": "Are the weeds the main issue, or is it more just general cleanup and overgrowth in the beds?",
            "Direct": "We do flower bed weeding too, and honestly it's one of those things that makes a huge visual difference."
        },
        "points": {
            "Shows off your plants": "Once the weeds are out, your actual flowers and plants can finally shine.",
            "Polished look": "Clean beds make the whole property look more cared for and put-together.",
            "Finishing touch": "Even a freshly mowed lawn can look incomplete if the beds are messy — this is the finishing touch.",
            "Low maintenance after": "Once we get them cleaned up, it's way easier to maintain going forward.",
            "Boosts curb appeal": "It's one of the first things people notice when they pull up to a house."
        },
        "closes": {
            "Soft": "Want me to add flower bed weeding so we can get the whole yard looking great?",
            "Assumptive": "Let's add the bed weeding — it'll really pull everything together and make the whole property pop.",
            "Question": "Would it make sense to have us tackle the beds while we're already there?"
        },
        "pro_tip": "Use the 'finishing touch' angle — even a freshly mowed lawn can look incomplete if the beds are messy. Frame it as the difference between 'good' and 'wow.'"
    },
    "Full Curb Appeal Bundle": {
        "triggers": ["Getting ready to sell", "Want the whole yard done", "Just moved in", "Event coming up", "Family visiting", "Make it look brand new"],
        "openings": {
            "Empathetic": "When you're prepping for something big, the last thing you want is to stress about the yard. I totally get wanting it all handled at once.",
            "Curious": "What's the occasion? Just want to make sure we set you up with everything you need to get it looking perfect.",
            "Direct": "If you're going for a full transformation, we can bundle everything together and really make the whole property pop."
        },
        "points": {
            "Complete transformation": "We can do mowing, bush trimming, flower bed weeding, and leaf removal if needed — the whole package.",
            "One crew handles it all": "Instead of coordinating multiple services, one crew takes care of everything in one visit.",
            "Saves time and stress": "You don't have to think about it or manage different appointments — we've got it covered.",
            "Perfect for selling": "If you're selling, this is exactly what gets buyers to say 'wow' when they pull up.",
            "Great for events": "If you've got family coming or an event, this is the fastest way to get the yard guest-ready."
        },
        "closes": {
            "Soft": "Want me to put together the full bundle so you don't have to worry about any of it?",
            "Assumptive": "Let's do the full curb appeal package — that way you're covered and the whole property will look amazing.",
            "Question": "Would it be easier to just bundle it all and knock it out in one visit?"
        },
        "pro_tip": "When someone has a big event or is selling, they're already in 'get it done' mode. Don't be shy about suggesting the full bundle — they'll appreciate you making it easy."
    }
}

SCRIPT_URL = "https://script.google.com/a/macros/lawnstarter.com/s/AKfycbyEGIP63SoZrL5XAAzfpY7NfaThcMIf_R36_YebHHsRkIeUWGfCmzVRHxI1OVs_WFNv/exec"

st.markdown('<div class="main-header"><h1>🌱 The <span class="highlight">Cutting Edge</span></h1></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📚 Flashcards", "📉 Loss Tracker", "🛠️ Guide Builder", "🎯 Attach Builder"])

with tab1:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Identify the WHY, then match the right response!</p>', unsafe_allow_html=True)
    if 'card_index' not in st.session_state:
        st.session_state.card_index = 0
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'completed' not in st.session_state:
        st.session_state.completed = []
    categories = ["All"] + list(set([o["category"] for o in objections]))
    selected_cat = st.selectbox("Filter by category:", categories)
    filtered = objections if selected_cat == "All" else [o for o in objections if o["category"] == selected_cat]
    if st.session_state.card_index >= len(filtered):
        st.session_state.card_index = 0
    current = filtered[st.session_state.card_index]
    progress = len([c for c in st.session_state.completed if c in [o["id"] for o in filtered]])
    st.progress(progress / len(filtered))
    st.markdown(f'<p style="text-align:right;color:#e8f5e6;">{progress} / {len(filtered)} reviewed</p>', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="card">
        <span class="category-badge">{current["category"]}</span>
        <span style="float:right;color:#888;">{st.session_state.card_index + 1} of {len(filtered)}</span>
        <div class="surface-text">"{current["surface"]}"</div>
        <p class="reason-label">🎯 THE REAL REASON</p>
        <p class="reason-text">{current["reason"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.session_state.show_answer:
        st.markdown(f'''
        <div class="card" style="background: linear-gradient(135deg, #e8f5e6, #d4edda);">
            <p class="approach-label">✅ BEST APPROACH</p>
            <p class="approach-text">{current["rebuttal"]}</p>
        </div>
        ''', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Flip Card", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()
    with col2:
        if st.button("➡️ Next Card", use_container_width=True):
            if current["id"] not in st.session_state.completed:
                st.session_state.completed.append(current["id"])
            st.session_state.card_index = (st.session_state.card_index + 1) % len(filtered)
            st.session_state.show_answer = False
            st.rerun()
    with col3:
        if st.button("🔁 Reset", use_container_width=True):
            st.session_state.completed = []
            st.session_state.card_index = 0
            st.session_state.show_answer = False
            st.rerun()

with tab2:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Track dispositions. Find patterns. Coach smarter.</p>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3 style="color:#2d5a27;">Log a Loss</h3>', unsafe_allow_html=True)
    agent_name = st.text_input("Agent Name")
    agent_id = st.text_input("Agent ID")
    disposition = st.selectbox("Disposition", ["Select disposition..."] + dispositions)
    if st.button("📤 Log & Send to Sheet", use_container_width=True):
        if agent_name and agent_id and disposition != "Select disposition...":
            timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
            params = urllib.parse.urlencode({"agentName": agent_name, "agentId": agent_id, "disposition": disposition, "timestamp": timestamp})
            full_url = f"{SCRIPT_URL}?{params}"
            st.markdown(f'<div class="success-box">✓ Logged: {disposition}</div>', unsafe_allow_html=True)
            st.markdown(f'<a href="{full_url}" target="_blank"><button style="width:100%;padding:10px;margin-top:10px;background:#4a9c3d;color:white;border:none;border-radius:10px;font-weight:bold;cursor:pointer;">Click here to send to Google Sheet</button></a>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all fields!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Build your own approach — your words, your style!</p>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3 style="color:#2d5a27;">🛠️ Build Your Guide</h3>', unsafe_allow_html=True)
    scenario = st.selectbox("What objection are you handling?", ["Select a scenario..."] + list(guide_scenarios.keys()))
    if scenario != "Select a scenario...":
        data = guide_scenarios[scenario]
        st.markdown("---")
        st.markdown("**Step 1: How do you want to open?**")
        opening_style = st.radio("Choose your style:", list(data["openings"].keys()), horizontal=True, key="guide_opening")
        st.markdown("---")
        st.markdown("**Step 2: Which points do you want to hit?**")
        selected_points = []
        for point_name, point_text in data["points"].items():
            if st.checkbox(point_name, key=f"guide_{scenario}_{point_name}"):
                selected_points.append(point_text)
        st.markdown("---")
        st.markdown("**Step 3: How do you want to close?**")
        close_style = st.radio("Choose your close:", list(data["closes"].keys()), horizontal=True, key="guide_close")
        if selected_points:
            st.markdown("---")
            st.markdown("### 📋 Your Custom Guide")
            guide_html = f'''
            <div class="guide-output">
                <div class="guide-section">
                    <p class="guide-label">🎯 Your Opening</p>
                    <p class="guide-text">"{data["openings"][opening_style]}"</p>
                </div>
                <div class="guide-section">
                    <p class="guide-label">💡 Key Points to Hit</p>
                    <ul style="color:#2d5a27; line-height: 1.8;">
            '''
            for point in selected_points:
                guide_html += f'<li style="margin-bottom:10px;">{point}</li>'
            guide_html += f'''
                    </ul>
                </div>
                <div class="guide-section">
                    <p class="guide-label">🎬 Your Close</p>
                    <p class="guide-text">"{data["closes"][close_style]}"</p>
                </div>
            </div>
            '''
            st.markdown(guide_html, unsafe_allow_html=True)
        else:
            st.info("👆 Select at least one key point to see your guide!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Build your attach pitch — your words, your style!</p>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3 style="color:#2d5a27;">🎯 Build Your Attach Pitch</h3>', unsafe_allow_html=True)
    attach_service = st.selectbox("What service do you want to attach?", ["Select a service..."] + list(attach_guides.keys()))
    if attach_service != "Select a service...":
        adata = attach_guides[attach_service]
        triggers_display = " • ".join([f'"{t}"' for t in adata["triggers"]])
        st.markdown(f'''
        <div style="background:#e8f5e6; padding:12px; border-radius:10px; margin:10px 0;">
            <p style="color:#2d5a27; margin:0; font-size:0.85rem;"><strong>🎧 Listen for:</strong> {triggers_display}</p>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Step 1: How do you want to open?**")
        attach_opening = st.radio("Choose your style:", list(adata["openings"].keys()), horizontal=True, key="attach_opening")
        st.markdown("---")
        st.markdown("**Step 2: Which points do you want to hit?**")
        selected_attach_points = []
        for point_name, point_text in adata["points"].items():
            if st.checkbox(point_name, key=f"attach_{attach_service}_{point_name}"):
                selected_attach_points.append(point_text)
        st.markdown("---")
        st.markdown("**Step 3: How do you want to close?**")
        attach_close = st.radio("Choose your close:", list(adata["closes"].keys()), horizontal=True, key="attach_close")
        if selected_attach_points:
            st.markdown("---")
            st.markdown("### 📋 Your Attach Pitch")
            attach_html = f'''
            <div class="guide-output">
                <div class="guide-section">
                    <p class="guide-label">🎯 Your Opening</p>
                    <p class="guide-text">"{adata["openings"][attach_opening]}"</p>
                </div>
                <div class="guide-section">
                    <p class="guide-label">💡 Key Points to Hit</p>
                    <ul style="color:#2d5a27; line-height: 1.8;">
            '''
            for point in selected_attach_points:
                attach_html += f'<li style="margin-bottom:10px;">{point}</li>'
            attach_html += f'''
                    </ul>
                </div>
                <div class="guide-section">
                    <p class="guide-label">🎬 Your Close</p>
                    <p class="guide-text">"{adata["closes"][attach_close]}"</p>
                </div>
            </div>
            '''
            st.markdown(attach_html, unsafe_allow_html=True)
            st.markdown(f'''
            <div class="card" style="background: linear-gradient(135deg, #f5a623, #f7b942); border-top: none; margin-top:15px;">
                <h4 style="color:#2d5a27; margin-bottom:10px;">💡 Pro Tip for {attach_service}</h4>
                <p style="color:#2d5a27; margin:0;">{adata["pro_tip"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("👆 Select at least one key point to see your pitch!")
    st.markdown('</div>', unsafe_allow_html=True)
