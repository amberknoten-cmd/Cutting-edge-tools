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

qa_questions = [
    {
        "category": "Greeting & Opening",
        "scenario": "A customer calls in. What's the FIRST thing you should do?",
        "options": {
            "A": "Ask for their address right away to check availability",
            "B": "Give the standard greeting and ask what they're looking for",
            "C": "Tell them about current promotions",
            "D": "Ask if they've used LawnStarter before"
        },
        "correct": "B",
        "explanation": "Always start with the standard greeting: 'Hello, this is [NAME] and thank you for calling LawnStarter. Would you mind sharing a bit about what you're looking for?' This sets a professional tone and lets the customer lead with their needs."
    },
    {
        "category": "Greeting & Opening",
        "scenario": "You're calling a customer who was texting with a colleague. What's the correct SMS greeting?",
        "options": {
            "A": "Hi, I'm calling about your lawn service inquiry",
            "B": "Hi, this is ___ with LawnStarter, you were just texting my colleague and they asked me to give you a call. How can I help?",
            "C": "Hello, is this the homeowner?",
            "D": "Hi, are you still interested in lawn service?"
        },
        "correct": "B",
        "explanation": "The SMS greeting should reference that they were texting a colleague: 'Hi, this is ___ with LawnStarter, you were just texting my colleague and they asked me to give you a call. How can I help?' This provides context and a smooth transition."
    },
    {
        "category": "Greeting & Opening",
        "scenario": "After the customer shares what they're looking for, what's a good way to acknowledge their response?",
        "options": {
            "A": "Okay, let me transfer you",
            "B": "Yes! We can take care of all of that! / I can help you with that / Let me look into that for you",
            "C": "That's not really what we do",
            "D": "Can you repeat that?"
        },
        "correct": "B",
        "explanation": "Acknowledge positively and focus on their main interest. Examples: 'Yes! We can take care of all of that!' or 'I can help you with that' or 'Let me look into that for you.' Then ask if they need anything else while we're out there."
    },
    {
        "category": "Verification",
        "scenario": "You need to verify a customer's information. What three things MUST you confirm?",
        "options": {
            "A": "Name, email, and credit card",
            "B": "Address, phone number, and email",
            "C": "Name, address (with zip), and phone number",
            "D": "Phone number, frequency preference, and budget"
        },
        "correct": "C",
        "explanation": "Verification requires: Phone number (mobile or landline), Address (street number, name AND zip), and Name. Email comes later during final verification."
    },
    {
        "category": "Verification",
        "scenario": "When verifying the customer's email at the end of the call, how should you read it back?",
        "options": {
            "A": "Just say the email quickly",
            "B": "Spell it out phonetically (PHONETICALLYSPELLEDOUT@ALWAYS.com)",
            "C": "Ask them to spell it for you",
            "D": "Send a confirmation text instead"
        },
        "correct": "B",
        "explanation": "Always read the email back phonetically to avoid errors. For example: 'I have your email J-O-H-N-D-O-E at G-M-A-I-L dot com.' This prevents miscommunication and ensures accuracy."
    },
    {
        "category": "Price Presentation",
        "scenario": "When presenting the price, what fee must ALWAYS be mentioned separately?",
        "options": {
            "A": "Long grass fee",
            "B": "Tax fee",
            "C": "$3.99 Trust and Safety fee",
            "D": "Cancellation fee"
        },
        "correct": "C",
        "explanation": "Always present: Base Price + $3.99 Trust and Safety fee. This fee helps cover pro vetting and potential property damage mediation. We itemize it for transparency rather than rolling it into the price."
    },
    {
        "category": "Price Presentation",
        "scenario": "A customer asks 'Does the price include taxes?' What should you say?",
        "options": {
            "A": "Yes, taxes are included",
            "B": "This price does not include taxes. Taxes are based on the local laws in your area.",
            "C": "There are no taxes on lawn services",
            "D": "I don't know, you'll have to check your bill"
        },
        "correct": "B",
        "explanation": "Always clarify: 'This price does not include taxes. Taxes are based on the local laws in your area.' Be transparent so there are no surprises on their bill."
    },
    {
        "category": "Price Presentation",
        "scenario": "What services are included in the base lawn mowing price?",
        "options": {
            "A": "Just mowing",
            "B": "Mowing, trimming edges, and blowing off paved surfaces",
            "C": "Mowing, fertilizing, and weed control",
            "D": "Mowing and leaf removal"
        },
        "correct": "B",
        "explanation": "The base mowing service includes: mowing, trimming edges, and blowing off paved surfaces. Also mention the free mobile app and web login for requesting additional services, making account changes, and contacting support."
    },
    {
        "category": "3-Cut Minimum",
        "scenario": "A customer says 'I only need a one-time mow.' What should you do FIRST?",
        "options": {
            "A": "Tell them about the 3-cut minimum immediately",
            "B": "Acknowledge and find out WHY they only want one mow",
            "C": "Offer them a discount to commit to 3 cuts",
            "D": "Transfer them to a supervisor"
        },
        "correct": "B",
        "explanation": "FIRST acknowledge and probe to find out why. Are they selling? Seasonal need? HOA notice? Understanding the reason helps you address their specific concern before discussing the 3-cut minimum."
    },
    {
        "category": "3-Cut Minimum",
        "scenario": "A customer says they're selling their home and only need one mow. What's a good response?",
        "options": {
            "A": "Sorry, we can't help with that",
            "B": "Identify when they're moving, mention single mows elsewhere cost the same, emphasize short-term commitment and getting on schedule now",
            "C": "We can waive the 3-cut minimum for you",
            "D": "You should hire a neighbor instead"
        },
        "correct": "B",
        "explanation": "For selling/moving: Identify when (have they moved already?), note that single mows with other companies are often the same price, emphasize short-term commitment, and create urgency to get on the schedule now."
    },
    {
        "category": "3-Cut Minimum",
        "scenario": "A customer got an HOA notice and says they just need one mow. How should you respond?",
        "options": {
            "A": "We only do 3 cuts, sorry",
            "B": "Long grass means recurring service can help restore the lawn, use us as backup if it happens again, get on schedule now for urgency",
            "C": "You should call your HOA",
            "D": "We can come today if you pay extra"
        },
        "correct": "B",
        "explanation": "For HOA situations: Explain that recurring service helps restore the lawn's look, they can use us as backup if it happens again, and create urgency to get on the schedule now before it gets worse."
    },
    {
        "category": "3-Cut Minimum",
        "scenario": "How should you explain the 48-hour rescheduling policy?",
        "options": {
            "A": "You can never change your schedule",
            "B": "Just let us know 48 hours before the next scheduled cut if you want to make changes",
            "C": "You have to call to cancel each time",
            "D": "Changes require a fee"
        },
        "correct": "B",
        "explanation": "Explain it simply: 'If at any point you would like to make changes to your schedule, just let us know 48 hours before the next scheduled cut.' This emphasizes flexibility while setting clear expectations."
    },
    {
        "category": "Scheduling",
        "scenario": "When providing the service window, what must you always include?",
        "options": {
            "A": "Just the days (Wednesday or Thursday)",
            "B": "Just the dates (July 20th or 21st)",
            "C": "Days AND dates (Wednesday or Thursday, July 20th or 21st)",
            "D": "An exact arrival time"
        },
        "correct": "C",
        "explanation": "Always provide the two-day window with BOTH days AND dates: 'Wednesday or Thursday, starting July 20th or 21st.' Never promise exact times."
    },
    {
        "category": "Scheduling",
        "scenario": "A customer says 'I don't want to wait around all day for the crew.' What should you tell them?",
        "options": {
            "A": "You have to be home for the service",
            "B": "It's contactless - no need to be home. The two-day window allows for weather and routing adjustments.",
            "C": "We can give you an exact time",
            "D": "You can call the day before to find out"
        },
        "correct": "B",
        "explanation": "Emphasize: It's contactless, so no need to be home. The two-day window allows for adjustments due to weather and routing. Also mention the delayed billing/quality check (3-4 days after service)."
    },
    {
        "category": "Scheduling",
        "scenario": "A customer says they need to be home to provide access. What solutions should you offer?",
        "options": {
            "A": "We can't service properties that need access",
            "B": "Can leave notes for gate codes or instructions, and message the pro in advance",
            "C": "You'll have to take the day off work",
            "D": "We only service properties with no gates"
        },
        "correct": "B",
        "explanation": "Offer solutions: They can leave notes with gate codes or special instructions, and message the pro in advance once assigned. This addresses their concern while keeping the flexible window."
    },
    {
        "category": "Scheduling",
        "scenario": "If a customer expresses flexibility with early or late service windows, what should you do?",
        "options": {
            "A": "Only mark one option",
            "B": "Acknowledge their agreement, mark BOTH options, and proceed accordingly",
            "C": "Tell them to decide later",
            "D": "Mark neither and let the pro decide"
        },
        "correct": "B",
        "explanation": "If the customer is flexible, acknowledge their agreement, mark BOTH early and late options, and proceed. This gives more scheduling flexibility while honoring their preferences."
    },
    {
        "category": "Long Grass Fee",
        "scenario": "At what height does the long grass fee potentially apply?",
        "options": {
            "A": "Over 6 inches",
            "B": "Over 9 inches",
            "C": "Over 12 inches",
            "D": "Over 15 inches"
        },
        "correct": "B",
        "explanation": "If grass is over 9 inches, a fee up to the full base mowing price may apply. If over 15 inches, the crew submits a quote for approval before servicing. Always mention this so there are no surprises!"
    },
    {
        "category": "Long Grass Fee",
        "scenario": "What happens if the grass is over 15 inches?",
        "options": {
            "A": "We refuse to service it",
            "B": "The crew will submit a quote for you to approve before servicing",
            "C": "We charge triple the base price automatically",
            "D": "We mow it but charge later"
        },
        "correct": "B",
        "explanation": "If grass is over 15 inches, the crew will submit a quote for the customer to approve BEFORE servicing. This ensures transparency and customer approval for heavily overgrown lawns."
    },
    {
        "category": "Long Grass Fee",
        "scenario": "A customer asks 'How do I know you aren't just charging extra for long grass?' What's the BEST response?",
        "options": {
            "A": "You'll just have to trust us",
            "B": "Pros must submit photos, you get an email when it's assessed, and you can dispute during the 3-day quality check",
            "C": "We never charge extra unfairly",
            "D": "You can call support if you disagree"
        },
        "correct": "B",
        "explanation": "Address with specifics: Pros must supply photos, you get an email immediately, there's a 3-day quality check before charging, and you can dispute with photo review. This builds trust through transparency."
    },
    {
        "category": "Long Grass Fee",
        "scenario": "A customer asks 'Why should I pay extra for long grass?' What's the BEST response?",
        "options": {
            "A": "Because that's our policy",
            "B": "We compensate our pros for additional work. Overgrown lawns take more time and create more wear and tear on equipment.",
            "C": "Everyone charges this",
            "D": "You can refuse and we won't mow"
        },
        "correct": "B",
        "explanation": "Explain the VALUE: We compensate our pros for additional work. Overgrown lawns take more time and create more wear and tear on equipment. This helps them understand it's fair, not arbitrary."
    },
    {
        "category": "Objection Handling",
        "scenario": "What's the correct ORDER for handling objections?",
        "options": {
            "A": "Lead with policies, then explain benefits",
            "B": "Acknowledge, clarify/probe why, then address with value",
            "C": "Offer a discount immediately, then explain",
            "D": "Transfer to a supervisor for approval"
        },
        "correct": "B",
        "explanation": "The correct order: 1) Acknowledge or show understanding, 2) Clarify or probe to find out why, 3) Address with value (what's the benefit?). Never lead with limitations and policies!"
    },
    {
        "category": "Objection Handling",
        "scenario": "What should you NEVER do when handling objections?",
        "options": {
            "A": "Show understanding",
            "B": "Lead with limitations and policies",
            "C": "Probe to find out why",
            "D": "Address with value"
        },
        "correct": "B",
        "explanation": "NEVER lead with limitations and policies. This puts the customer on the defensive. Instead, acknowledge, probe, then address with value and benefits. Policies should support your solution, not lead it."
    },
    {
        "category": "48-Hour Window",
        "scenario": "A customer says 'I have an HOA notice and need service TODAY.' What should you tell them?",
        "options": {
            "A": "Sorry, we can't help with urgent requests",
            "B": "We have the fastest turnaround, and once assigned you can message your pro about availability",
            "C": "I'll see if I can get a supervisor to approve same-day service",
            "D": "You should try a different company"
        },
        "correct": "B",
        "explanation": "Emphasize we have the fastest turnaround time in the industry. Once a pro is assigned, they can message them directly about availability. Also mention we can send a confirmation email they can forward to their HOA."
    },
    {
        "category": "48-Hour Window",
        "scenario": "A customer asks 'Why do I have to wait 48 hours?' What should you explain?",
        "options": {
            "A": "Because that's just how it works",
            "B": "Routes are planned in advance and it gives us time to find a pro. Want me to hold a spot?",
            "C": "Our pros are lazy",
            "D": "We're understaffed"
        },
        "correct": "B",
        "explanation": "Explain: Routes are planned in advance and it gives us time to find a pro in your area. Then offer to hold a spot. This turns a limitation into an action step."
    },
    {
        "category": "Cross-Selling",
        "scenario": "When offering Lawn Treatment, what should you highlight about the service?",
        "options": {
            "A": "It's required for all customers",
            "B": "It includes fertilizer, weed control, and pre-emergent with 7-8 rounds per year",
            "C": "It replaces the need for mowing",
            "D": "It's only available in the summer"
        },
        "correct": "B",
        "explanation": "Lawn Treatment includes fertilizer, weed control, and pre-emergent. For best results: 7-8 rounds per year, every 4-6 weeks. They won't be charged until service is complete. Mention that weed-free lawns can reduce mowing costs!"
    },
    {
        "category": "Cross-Selling",
        "scenario": "What should you tell New York customers about Lawn Treatment?",
        "options": {
            "A": "It's not available in New York",
            "B": "We currently only offer fertilization in your area",
            "C": "It's the same as everywhere else",
            "D": "They get a discount"
        },
        "correct": "B",
        "explanation": "For New York customers specifically: 'We currently only offer fertilization in your area.' This sets correct expectations about what's available in their region."
    },
    {
        "category": "Cross-Selling",
        "scenario": "If a customer says NO to an additional service, what should you do?",
        "options": {
            "A": "Keep pushing until they say yes",
            "B": "Just move on without saying anything",
            "C": "Remind them it can be added anytime via the app/portal",
            "D": "Offer a bigger discount"
        },
        "correct": "C",
        "explanation": "If they say no, remind them they can always add services anytime via the app or portal, or contact support for services not available there. Don't push, but leave the door open!"
    },
    {
        "category": "Cross-Selling",
        "scenario": "When cross-selling Leaf Removal, what should you ask to identify the need?",
        "options": {
            "A": "Do you want leaf removal?",
            "B": "Are there any leaves or small twigs on your lawn?",
            "C": "Is it fall time?",
            "D": "Do you have trees?"
        },
        "correct": "B",
        "explanation": "Ask specifically: 'Are there any leaves or small twigs on your lawn?' This identifies the actual need. If yes, offer the IQ Cleanup quote and set expectations about what happens if excessive leaves are found at service time."
    },
    {
        "category": "Cross-Selling",
        "scenario": "What expectation should you set about leaves and mowing?",
        "options": {
            "A": "We always mow over leaves",
            "B": "If excessive leaves need to be picked up before mowing, we'll quote for cleanup which could delay service completion",
            "C": "We never mow if there are leaves",
            "D": "Leaves don't affect mowing"
        },
        "correct": "B",
        "explanation": "Set the expectation: 'If the crew arrives and there's an excessive amount of leaves that need picked up before we can mow, we'll need to quote you for the cleanup, wait for your approval, which could prolong your service completion.'"
    },
    {
        "category": "Cross-Selling",
        "scenario": "When pitching Lawn Treatment, what optional benefit can you mention about weeds and mowing?",
        "options": {
            "A": "Weeds make lawns look nicer",
            "B": "Weeds grow first, make lawns appear overgrown, and controlling them can reduce mowing frequency and costs",
            "C": "Weeds have no effect on mowing",
            "D": "We charge less if you have weeds"
        },
        "correct": "B",
        "explanation": "Optional context: Weeds are the first to grow, making the lawn appear overgrown or warrant additional fees. Keeping weeds in check minimizes overall growth, reducing the need for more frequent mowing. This adds value to the Lawn Treatment pitch!"
    },
    {
        "category": "Property Details",
        "scenario": "A customer has outdoor pets. What TWO things should you tell them?",
        "options": {
            "A": "We can't service properties with pets",
            "B": "Pets should be secured during service AND please pick up pet waste",
            "C": "The pro will handle the pets",
            "D": "They need to pay an extra pet fee"
        },
        "correct": "B",
        "explanation": "Two requirements: 1) Pets should be secured during service time, 2) Please pick up any pet waste on the property. If excessive waste is found, the crew will mow around it."
    },
    {
        "category": "Property Details",
        "scenario": "A customer has a property gate. What should you ask?",
        "options": {
            "A": "Just ask if they have a gate",
            "B": "Ask if it's wide enough for a riding mower, if it's a gated community, and if there's a code or special instructions",
            "C": "Tell them we can't service gated properties",
            "D": "Ask them to leave it open forever"
        },
        "correct": "B",
        "explanation": "For property gates: Is it wide enough for a riding mower? For community gates: Is there a gate code or special instructions? Include access details in the 'Special Neighborhood Access' field. Be concise!"
    },
    {
        "category": "Property Details",
        "scenario": "Where should you include special access details?",
        "options": {
            "A": "Just tell the customer verbally",
            "B": "In the 'Special Neighborhood Access' field on the work order",
            "C": "In an email to the pro",
            "D": "Nowhere, the pro will figure it out"
        },
        "correct": "B",
        "explanation": "Include special access details in the 'Special Neighborhood Access' field on the work order. Keep in mind the importance of being concise so the information is clear and usable."
    },
    {
        "category": "Payment",
        "scenario": "A customer asks 'Why do I have to put a card on file?' What's the BEST response?",
        "options": {
            "A": "It's just our policy",
            "B": "You don't need to be home, we charge 3 days AFTER service so you can address any issues first",
            "C": "We need it for security purposes",
            "D": "You can pay cash if you prefer"
        },
        "correct": "B",
        "explanation": "Focus on benefits: No need to be home when service happens, and we charge 3 days AFTER completion — giving time to address any service issues before being charged. We send notifications when service is complete."
    },
    {
        "category": "Payment",
        "scenario": "When collecting payment info, what do you tell the customer?",
        "options": {
            "A": "Give me your card number",
            "B": "I'm sending a secure link via text and email since we don't have access to payment info on our end",
            "C": "You can pay after the first service",
            "D": "We'll call back later for payment"
        },
        "correct": "B",
        "explanation": "Always say: 'I'm sending over a secure link for you to add your payment info directly, since we don't have access to that on our end. This will go through text and email.' We never take card info verbally!"
    },
    {
        "category": "Payment",
        "scenario": "A customer is worried about security with online payment. What can you tell them about Stripe?",
        "options": {
            "A": "I don't know anything about it",
            "B": "Stripe is highly secure and used by large businesses like Walmart and Amazon, used by millions",
            "C": "It's pretty safe I guess",
            "D": "You can mail a check instead"
        },
        "correct": "B",
        "explanation": "Reassure them: Stripe is highly secure and used by large businesses like Walmart and Amazon — used by millions. Also remind them we charge 3 days after completion and send notifications when service is done."
    },
    {
        "category": "Payment",
        "scenario": "A customer says 'I don't like recurring charges.' What should you emphasize?",
        "options": {
            "A": "You have to accept them",
            "B": "We only charge if a service is completed, send notifications when done, and charge 3 days AFTER service",
            "C": "You can cancel anytime",
            "D": "Everyone does recurring charges"
        },
        "correct": "B",
        "explanation": "Emphasize: We only charge if a service is completed. We send email and app notifications as soon as service is done. We only charge 3 days AFTER the service. This gives them control and transparency."
    },
    {
        "category": "Closing",
        "scenario": "What should you tell the customer to expect AFTER the call?",
        "options": {
            "A": "Nothing, just say goodbye",
            "B": "Email when a pro picks up the job, text with app link and temp password, and they can message the pro directly",
            "C": "A pro will call them back",
            "D": "They need to call back to confirm"
        },
        "correct": "B",
        "explanation": "Set expectations: 1) Email confirming a pro picked up the job + their two-day window, 2) Text with app link and temporary password (email is username), 3) They can message their pro directly once assigned!"
    },
    {
        "category": "Closing",
        "scenario": "What's the LAST thing you should do before ending the call?",
        "options": {
            "A": "Hang up quickly to take the next call",
            "B": "Ask 'Any other questions before I let you go?' and direct them to support via app/portal",
            "C": "Try to sell one more service",
            "D": "Transfer them to QA"
        },
        "correct": "B",
        "explanation": "Always ask 'Any other questions before I let you go?' Then direct them to the Support Team via app or portal for future questions. End with 'Thank you for choosing LawnStarter. Have a great day!'"
    },
    {
        "category": "Closing",
        "scenario": "For landline-only customers, how should you explain logging into the website?",
        "options": {
            "A": "They can't use the website",
            "B": "Enter email address, click forgot password, receive temp password via email, change password once logged in",
            "C": "Call support for help",
            "D": "They have to use the app instead"
        },
        "correct": "B",
        "explanation": "For landline customers: 'Enter your email address and click the forgot your password option. You'll receive an email with a temporary password. Make sure to change the password once you log in.' This helps non-app users access their account."
    },
    {
        "category": "Closing",
        "scenario": "What referral opportunity should you mention in the introduction email?",
        "options": {
            "A": "There's no referral program",
            "B": "Recommend us on NextDoor and receive a $20 credit to your account",
            "C": "Refer friends for a discount",
            "D": "Leave a Google review for $50"
        },
        "correct": "B",
        "explanation": "Mention: 'In your introduction email, you will see a button about recommending us on NextDoor. Do this and receive a $20 credit to your account.' This encourages referrals and rewards the customer."
    },
    {
        "category": "Not DM",
        "scenario": "You're speaking with someone who ISN'T the decision maker. What's REQUIRED before ending the call?",
        "options": {
            "A": "Just say goodbye and call back later",
            "B": "Educate on value and offer to hold a spot",
            "C": "Ask them to have the DM call back",
            "D": "Send an email to the DM"
        },
        "correct": "B",
        "explanation": "When speaking with non-DM: Probe if DM is available, educate on value (flexibility, app benefits, quality check), and ALWAYS offer to hold a spot. Holding a spot is REQUIRED for non-DM calls."
    },
    {
        "category": "Not DM",
        "scenario": "If the decision maker IS available when you're speaking with a non-DM, what should you do?",
        "options": {
            "A": "Just continue with the non-DM",
            "B": "Offer to speak with the decision maker",
            "C": "Ask them to call back",
            "D": "End the call"
        },
        "correct": "B",
        "explanation": "If the DM is available, offer to speak with them directly. This gives you the best chance of closing the sale with the person who can actually make the decision."
    },
    {
        "category": "Not DM",
        "scenario": "If the DM is NOT available, what should you ask the non-DM?",
        "options": {
            "A": "When will they be back?",
            "B": "Does the DM have specific needs or concerns?",
            "C": "Can they make the decision instead?",
            "D": "Should we call back tomorrow?"
        },
        "correct": "B",
        "explanation": "Ask: 'Does [DM] have specific needs or concerns?' This helps you understand what's important to the actual decision maker so you can address those points and educate on value."
    },
    {
        "category": "Trust & Safety Fee",
        "scenario": "A customer asks 'Why do I have to pay the Trust & Safety fee?' What should you say?",
        "options": {
            "A": "It's just an extra charge we add",
            "B": "It helps cover pro vetting and mediate potential property damage — most companies roll it into price, we itemize for transparency",
            "C": "You can skip it if you want",
            "D": "It's a government requirement"
        },
        "correct": "B",
        "explanation": "The T&S fee covers the pro vetting process and helps mediate potential property damage. Most companies roll it into their price — we itemize it for transparency. Most local providers don't provide any coverage at all!"
    },
    {
        "category": "Frequency Objections",
        "scenario": "A customer says 'I don't want to be locked into a schedule.' What should you emphasize?",
        "options": {
            "A": "You have to commit to the schedule",
            "B": "Flexible options: reschedule, skip, pause — manage via app or message your pro — can change frequency as needed",
            "C": "Just cancel if you don't like it",
            "D": "We'll call you before each service"
        },
        "correct": "B",
        "explanation": "Emphasize flexibility: reschedule, skip, or pause options. Manage everything on the app or communicate with your pro directly. Can change frequency as needed. Regular maintenance = healthier lawn!"
    },
    {
        "category": "Subcontractor Objection",
        "scenario": "A customer says 'I don't want to work with subcontractors.' What should you tell them?",
        "options": {
            "A": "We don't use subcontractors",
            "B": "They're local vetted pros, our platform helps their business, there's a quality check, you can change pro anytime",
            "C": "You have no choice",
            "D": "We'll send our employees instead"
        },
        "correct": "B",
        "explanation": "Address the concern: They're local, vetted pros. Our platform helps local pros with their business. Explain the quality check. You can change pro anytime. It's a short-term commitment. This reframes 'subcontractor' positively."
    },
    {
        "category": "Order Recap",
        "scenario": "What must you include in the order recap?",
        "options": {
            "A": "Just the price",
            "B": "Frequency, price, T&S fee, two-day window with days and dates, and all additional services with their details",
            "C": "Just the service date",
            "D": "Only the customer's name"
        },
        "correct": "B",
        "explanation": "Full recap includes: frequency (weekly/biweekly/monthly), price, $3.99 T&S fee, two-day window with days AND dates, plus all additional services with their frequency expectations. For Lawn Treatment customers, mention they'll get an email about their first application."
    },
    {
        "category": "Scope & Frequency",
        "scenario": "What two things should you ask about scope and frequency?",
        "options": {
            "A": "Just ask about price",
            "B": "What area needs service (full, front, back) and how often (weekly, biweekly, monthly)",
            "C": "Only ask about the front yard",
            "D": "Ask what their neighbor pays"
        },
        "correct": "B",
        "explanation": "Ask about scope: What area needs service? Full yard, front, back? And frequency: How often? Weekly, biweekly, monthly (when available)? If they already told you, just confirm rather than asking again."
    }
]

faq_data = {
    "Pricing & Fees": [
        {
            "question": "What's included in the base mowing price?",
            "answer": "Mowing, trimming edges, and blowing off paved surfaces.",
            "phrasing": "Your mowing service covers the full package — we'll mow the lawn, trim up the edges, and blow off any grass clippings from your driveway and walkways."
        },
        {
            "question": "What is the Trust & Safety fee?",
            "answer": "$3.99 fee that covers pro vetting and helps mediate potential property damage. Most companies roll it into their price; we itemize for transparency.",
            "phrasing": "There's a small Trust and Safety fee that helps us vet all our pros and covers you in case of any property issues. Most companies just hide it in their price — we like to be upfront about it."
        },
        {
            "question": "Are taxes included in the price?",
            "answer": "No. Taxes are based on local laws and will be added based on your area.",
            "phrasing": "The price I quoted doesn't include taxes — those vary depending on where you're located, so they'll be calculated based on your local rates."
        },
        {
            "question": "Why are your prices higher than some competitors?",
            "answer": "Price includes insured professionals, quality guarantee, 3-day billing delay, dedicated support team, and platform convenience.",
            "phrasing": "Our price reflects what you're actually getting — verified, insured pros, a quality guarantee, and a whole support team behind you. Plus you don't pay until three days after service, so you can make sure everything looks good first."
        },
        {
            "question": "Can I get a discount?",
            "answer": "Check for qualified promotions. Don't lead with discounts — lead with value first.",
            "phrasing": "Let me see what we have available for you! But honestly, most people find the service pays for itself with the convenience and quality. Let me tell you what you're getting..."
        }
    ],
    "Scheduling & Service Windows": [
        {
            "question": "How does the two-day service window work?",
            "answer": "Service is scheduled within a two-day window (e.g., Wednesday or Thursday). Always provide both days AND dates.",
            "phrasing": "We schedule within a two-day window — so for example, your crew would come either Wednesday the 20th or Thursday the 21st. It gives us flexibility for weather and routing."
        },
        {
            "question": "Can I get an exact time for when the crew will arrive?",
            "answer": "No exact times. The two-day window allows for weather and routing adjustments. Service is contactless, so no need to be home.",
            "phrasing": "We can't promise an exact time since routes can shift with weather and other jobs, but the good news is you don't need to be home! It's totally contactless."
        },
        {
            "question": "Why do I have to wait 48 hours for the first service?",
            "answer": "Routes are planned in advance and it gives time to find a pro. This is still the fastest turnaround in the industry.",
            "phrasing": "The 48-hour window lets us get you matched with a great pro and fit you into the route. It's actually the fastest turnaround you'll find — most companies take way longer."
        },
        {
            "question": "I need service today — can you make an exception?",
            "answer": "Can't guarantee same-day, but once assigned they can message their pro through the app to ask about earlier availability.",
            "phrasing": "I wish I could guarantee today, but here's what I can do — once you're set up and a pro is assigned, you can message them directly through the app and ask if they can squeeze you in sooner. It's worth a shot!"
        },
        {
            "question": "What if I need to be home to provide access?",
            "answer": "They can leave gate codes or instructions in notes, and message the pro in advance once assigned.",
            "phrasing": "No problem! You can leave any gate codes or special instructions in your account, and once your pro is assigned you can message them directly to coordinate."
        },
        {
            "question": "What if it rains on my service day?",
            "answer": "The two-day window allows for weather adjustments. Pro will come on the alternate day if needed.",
            "phrasing": "That's exactly why we have the two-day window — if weather's bad on day one, they'll come on day two. You're covered either way."
        }
    ],
    "3-Cut Minimum": [
        {
            "question": "Why is there a 3-cut minimum?",
            "answer": "It's a short-term commitment that allows the pro to learn your lawn and preferences. Single mows elsewhere often cost the same.",
            "phrasing": "It's really just a short-term commitment — three cuts. And honestly, single mows from other companies usually cost about the same anyway. Plus your pro gets to know your lawn and your preferences."
        },
        {
            "question": "Can I get just one mow?",
            "answer": "No, but probe to find out WHY first. Address their specific situation (selling, seasonal, HOA, etc.) before discussing the minimum.",
            "phrasing": "I hear you — can I ask what's prompting the need for just one? [Then address their specific situation]"
        },
        {
            "question": "I'm selling my house and only need one mow.",
            "answer": "Identify timeline, note single mows elsewhere cost the same, emphasize short-term commitment and urgency to get on schedule.",
            "phrasing": "Oh congrats! When's the closing? The thing is, even one-time mows from other places usually run about the same price. And with just a 3-cut commitment, you can get on our schedule now and not worry about the lawn while you're dealing with everything else."
        },
        {
            "question": "I got an HOA notice — I just need it done once.",
            "answer": "Recurring service helps restore lawn health, can use as backup if it happens again, create urgency to get on schedule.",
            "phrasing": "I totally get the stress of that! Here's the thing — if it got bad enough for a notice, regular service will help get it back in shape and keep it there. And if this ever happens again, you've got us as backup. Let's get you on the schedule now before it gets worse."
        },
        {
            "question": "Can I cancel after the 3 cuts?",
            "answer": "Yes! Just let us know 48 hours before the next scheduled service. Very flexible.",
            "phrasing": "Absolutely! After your three cuts, if you want to stop or take a break, just let us know 48 hours before your next scheduled service. Super flexible."
        }
    ],
    "Payment & Billing": [
        {
            "question": "When do I get charged?",
            "answer": "3 days after service is completed. This allows time to address any issues before being charged.",
            "phrasing": "You won't be charged until three days after the service is done. That gives you time to check everything out and let us know if anything needs fixing before your card is charged."
        },
        {
            "question": "Why do I need a card on file?",
            "answer": "Allows contactless service (no need to be home), 3-day billing delay for quality assurance, and notifications when service is complete.",
            "phrasing": "It just makes everything easier — you don't have to be home, we don't charge until three days after so you can inspect the work first, and you'll get notifications as soon as the job's done."
        },
        {
            "question": "Can I pay with cash or check?",
            "answer": "No, only major credit/debit cards. Benefits: no need to be home, 3-day billing delay, bank protection.",
            "phrasing": "We only take cards, but honestly it's a benefit for you — you don't have to be home to pay anyone, and your bank has your back if there's ever any issue. Plus we don't charge until three days after."
        },
        {
            "question": "Is my card information secure?",
            "answer": "Yes, we use Stripe which is highly secure and used by Walmart, Amazon, and millions of businesses.",
            "phrasing": "Totally secure — we use Stripe, which is the same payment system that huge companies like Amazon and Walmart use. Millions of transactions every day."
        },
        {
            "question": "I don't like recurring charges.",
            "answer": "We only charge if a service is completed. Notifications are sent when service is done. 3-day delay before charge.",
            "phrasing": "I get that — but we only charge when a service is actually completed. You'll get a notification as soon as it's done, and you have three full days before we charge anything. So you're always in control."
        },
        {
            "question": "How do I add my payment info?",
            "answer": "A secure link is sent via text and email. Agents never take card info verbally.",
            "phrasing": "I'm going to send you a secure link by text and email — just click it and enter your card info there. We don't take payment info over the phone for security reasons."
        }
    ],
    "Long Grass Fee": [
        {
            "question": "What is the long grass fee?",
            "answer": "Industry standard fee if grass is over 9 inches — up to 100% of base mowing price. Over 15 inches requires a quote approval before servicing.",
            "phrasing": "It's an industry standard thing — if the grass is over 9 inches, there may be an additional fee up to double the base price because of the extra time and equipment wear. I'm mentioning it now so there are no surprises."
        },
        {
            "question": "Why do I have to pay extra for long grass?",
            "answer": "Compensates pros for additional work. Overgrown lawns take more time and cause more wear on equipment.",
            "phrasing": "Overgrown lawns take a lot more time and are harder on the equipment, so we make sure the pros are compensated fairly for that extra work."
        },
        {
            "question": "How do I know you won't just charge me unfairly?",
            "answer": "Pros must submit photos, you get an email immediately when assessed, 3-day quality check before charging, can dispute with photo review.",
            "phrasing": "Great question — the pro has to submit photos if they claim long grass. You'll get an email right away, and you have three days before you're charged to dispute it. We'll review the photos with you."
        },
        {
            "question": "What if my grass is over 15 inches?",
            "answer": "The crew will submit a quote for approval BEFORE servicing. No surprises.",
            "phrasing": "If it's really overgrown — over 15 inches — the crew will send you a quote to approve before they even start. So you'll know exactly what to expect."
        },
        {
            "question": "Will I always get charged the long grass fee?",
            "answer": "Usually only on first cut if lawn has been neglected. Regular service keeps it under control after that.",
            "phrasing": "Usually it only comes up on the first visit if the lawn's been let go for a while. Once you're on regular service, it stays under control and you won't see that fee."
        }
    ],
    "Cross-Selling Services": [
        {
            "question": "What's included in Lawn Treatment?",
            "answer": "Fertilizer, weed control, and pre-emergent. 7-8 rounds per year, every 4-6 weeks. Not charged until service is complete.",
            "phrasing": "It's a full lawn health package — fertilizer to green things up, weed control for what's already there, and pre-emergent to stop new weeds before they start. Usually 7 or 8 rounds a year for best results."
        },
        {
            "question": "Is Lawn Treatment available in New York?",
            "answer": "Only fertilization is available in NY — no weed control or pre-emergent.",
            "phrasing": "In New York we currently just offer the fertilization part — the weed control isn't available in your area yet."
        },
        {
            "question": "Why should I add Lawn Treatment?",
            "answer": "Weed-free lawns can reduce mowing frequency and costs. Weeds grow first and make lawn look overgrown faster.",
            "phrasing": "Here's a bonus — keeping weeds under control actually means your lawn grows more evenly, so you might not need mowing as often. Weeds are usually what make a lawn look overgrown fast."
        },
        {
            "question": "What if there are leaves on my lawn?",
            "answer": "Ask if there are leaves/twigs. Offer IQ Cleanup quote. Set expectation: excessive leaves may require cleanup quote before mowing.",
            "phrasing": "Are there any leaves or debris on the lawn right now? If so, I can get you a quote for cleanup so there are no surprises. If the crew shows up and there's a lot, they'd need to quote it before mowing anyway."
        },
        {
            "question": "What other services do you offer?",
            "answer": "Bush trimming, flower bed weeding, leaf removal, and in some areas: grub treatment, mosquito prevention, mulching, gutter cleaning, tree trimming, sod installation, etc.",
            "phrasing": "Beyond mowing, we do bush trimming, flower bed weeding, leaf removal — all the stuff that makes your yard look great. Depending on your area, we might also have things like mulching, tree trimming, and more."
        },
        {
            "question": "The customer said no to an add-on. What do I do?",
            "answer": "Don't push. Remind them they can add services anytime via the app or portal, or contact support.",
            "phrasing": "No problem at all! Just so you know, you can always add any of these services later right through the app whenever you need them."
        }
    ],
    "Property Details": [
        {
            "question": "What if I have pets outside?",
            "answer": "Pets should be secured during service. Request that pet waste be picked up beforehand. Excessive waste will be mowed around.",
            "phrasing": "Just make sure any pets are secured when the crew comes by, and if you could pick up any pet waste beforehand that's super helpful. If there's a lot, they'll just mow around it."
        },
        {
            "question": "What if I have a gate?",
            "answer": "Ask if it's wide enough for a riding mower. Get gate codes and special instructions. Include in Special Neighborhood Access field.",
            "phrasing": "Is the gate wide enough for a mower to fit through? And is there a code or anything special they need to know to get in? I'll make sure it's all in your account."
        },
        {
            "question": "Do I need to be home for the service?",
            "answer": "No! Service is contactless. Leave any special instructions or gate codes in your account.",
            "phrasing": "Nope, you don't need to be home at all! It's totally contactless. Just leave any instructions or codes in your account and you're good to go."
        },
        {
            "question": "What areas can be serviced?",
            "answer": "Full yard, front only, or back only. Ask the customer what area needs service.",
            "phrasing": "Did you need the full yard done, or just the front or back? We can do whatever works for you."
        },
        {
            "question": "What if I have special instructions for the crew?",
            "answer": "Include in Special Neighborhood Access field. Keep notes concise and clear. Can also message pro directly once assigned.",
            "phrasing": "I'll add that to your account notes, and once you're matched with a pro you can also message them directly through the app to go over any details."
        }
    ],
    "Cancellation & Rescheduling": [
        {
            "question": "How do I reschedule or skip a service?",
            "answer": "Let us know 48 hours before the next scheduled cut. Can manage via app or by contacting support.",
            "phrasing": "Just give us a heads up at least 48 hours before your next scheduled service. You can do it right in the app or reach out to support."
        },
        {
            "question": "Can I pause my service?",
            "answer": "Yes! Flexible options include reschedule, skip, or pause. Can change frequency as needed.",
            "phrasing": "Absolutely — you can skip, pause, or reschedule anytime. Just let us know 48 hours ahead. Totally flexible."
        },
        {
            "question": "What if I want to cancel completely?",
            "answer": "Can cancel with 48-hour notice before next service. Short-term commitment after 3-cut minimum is met.",
            "phrasing": "Once you've completed your three services, you can cancel anytime — just let us know 48 hours before your next scheduled cut."
        },
        {
            "question": "What's the 48-hour policy?",
            "answer": "Any changes to schedule must be made at least 48 hours before the next service. Applies to rescheduling, skipping, pausing, or canceling.",
            "phrasing": "We just ask for 48 hours notice before any scheduled service if you need to change, skip, or cancel. That gives us time to adjust the routes."
        }
    ],
    "App & Account": [
        {
            "question": "How do I access my account?",
            "answer": "Via mobile app (link sent by text) or web portal. Email is username, temporary password sent via text.",
            "phrasing": "You'll get a text with a link to download the app and a temporary password. Your email is your username. You can also use the website if you prefer."
        },
        {
            "question": "What can I do in the app?",
            "answer": "Request additional services, make account changes, message your pro, contact support, view service history.",
            "phrasing": "Pretty much everything — you can add services, make changes to your account, message your pro directly, and it's the fastest way to reach support if you need anything."
        },
        {
            "question": "What if I only have a landline?",
            "answer": "Go to website, enter email, click forgot password, receive temp password via email, change password once logged in.",
            "phrasing": "No problem — just go to the website, enter your email, and click 'forgot password.' You'll get a temporary password by email, then just update it once you're in."
        },
        {
            "question": "How do I message my pro?",
            "answer": "Through the app once a pro is assigned and picks up the job.",
            "phrasing": "Once a pro picks up your job, you'll be able to message them directly through the app. Great for coordinating access or asking questions."
        },
        {
            "question": "How do I contact support?",
            "answer": "Through the app or web portal — fastest method. Support team available to help.",
            "phrasing": "The fastest way is right through the app or website — there's a support option and the team is super responsive."
        }
    ],
    "Quality & Trust": [
        {
            "question": "How do I know the pro will do a good job?",
            "answer": "All pros are vetted and insured. 3-day quality check before billing. Dedicated quality team. Can change pro anytime.",
            "phrasing": "Every pro is vetted and insured before they can work with us. Plus you have three days to check the work before you're charged, and we have a whole team dedicated to fixing anything that's not right. And if you just don't click with your pro, you can request a different one."
        },
        {
            "question": "What if I'm not happy with the service?",
            "answer": "3-day quality check before charging. Report issues and they'll be fixed before payment. Dedicated quality team.",
            "phrasing": "You have three full days after service to look everything over. If anything's not right, let us know and we'll send someone to fix it — all before you're ever charged."
        },
        {
            "question": "Are the pros insured?",
            "answer": "Yes, all pros are verified and insured. Trust & Safety fee helps cover this.",
            "phrasing": "Every single one. They're all verified and insured before they can service any properties with us."
        },
        {
            "question": "Can I change my pro?",
            "answer": "Yes, anytime. Just contact support or request through the app.",
            "phrasing": "Absolutely — if you're not happy or just want someone different, just let us know through the app and we'll get you matched with someone new."
        },
        {
            "question": "I've never heard of your company.",
            "answer": "Encourage them to Google reviews. Mention no payment until 3 days after service, so they can see quality firsthand.",
            "phrasing": "That's fair! If you Google us, you'll see tons of great reviews from real customers. And since you don't pay until three days after service, you get to see the quality for yourself before any money changes hands."
        }
    ],
    "Not Decision Maker": [
        {
            "question": "What if I'm not speaking with the decision maker?",
            "answer": "Probe if DM is available. If not, ask about DM's specific needs/concerns. Educate on value. ALWAYS offer to hold a spot (required).",
            "phrasing": "Is [the homeowner/decision maker] available by chance? [If no] No worries! Do they have any specific concerns I could help address? Either way, I can hold a spot on the schedule so they don't miss out."
        },
        {
            "question": "The person wants to check with their spouse first.",
            "answer": "Totally fine. Offer to hold a spot. Mention no charge until after service and can cancel 48 hours before.",
            "phrasing": "Totally understand! Let me hold a spot for you while you chat with them — there's no charge until after service anyway, and you can cancel up to 48 hours before if you decide it's not for you."
        },
        {
            "question": "Do I need to hold a spot for non-DM calls?",
            "answer": "YES — holding a spot is REQUIRED for all non-DM calls.",
            "phrasing": "I'd love to hold a spot for you so the decision maker doesn't lose out on availability. No commitment — just keeps your options open!"
        }
    ],
    "Objection Handling": [
        {
            "question": "What's the right way to handle objections?",
            "answer": "1) Acknowledge or show understanding, 2) Clarify or probe to find out why, 3) Address with value (not policies). Never lead with limitations.",
            "phrasing": "First, let the customer know you hear them. Then ask questions to understand what's really going on. Finally, address their actual concern with how we can help — not just what our policies are."
        },
        {
            "question": "Customer says 'That's too expensive.'",
            "answer": "Acknowledge, probe why (comparing to someone else? budget concern?), then address with value — insurance, quality guarantee, 3-day billing, support team.",
            "phrasing": "I hear you — price is definitely a factor. Can I ask, is it more than you expected or are you comparing to another quote? [Then address] What you're getting is insured pros, a quality guarantee, and you don't pay until three days after when you've seen the work."
        },
        {
            "question": "Customer wants to think about it.",
            "answer": "Acknowledge, probe what's holding them back, offer to hold a spot (no commitment, can cancel 48 hrs before).",
            "phrasing": "Totally fair! Is there something specific you're weighing, or just want time to decide? Either way, I can hold a spot for you — no commitment, and you can cancel up to 48 hours before if you change your mind."
        },
        {
            "question": "Customer says they'll call back later.",
            "answer": "Acknowledge, create urgency (availability fills up), offer to hold spot with no commitment.",
            "phrasing": "No problem! Just keep in mind availability can fill up, so if you want I can grab a spot for you now — no commitment, just holds your place. Then you can cancel if you find something else."
        }
    ]
}

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 Flashcards", "📉 Loss Tracker", "🛠️ Guide Builder", "🎯 Attach Builder", "🎮 QA Game Show", "🔍 FAQ Search"])

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

with tab5:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Test your QA knowledge — game show style! 🎯</p>', unsafe_allow_html=True)
    
    if 'qa_index' not in st.session_state:
        st.session_state.qa_index = 0
    if 'qa_score' not in st.session_state:
        st.session_state.qa_score = 0
    if 'qa_answered' not in st.session_state:
        st.session_state.qa_answered = False
    if 'qa_selected' not in st.session_state:
        st.session_state.qa_selected = None
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    
    total_questions = len(qa_questions)
    current_q = qa_questions[st.session_state.qa_index]
    
    score_pct = (st.session_state.qa_score / max(len(st.session_state.qa_history), 1)) * 100 if st.session_state.qa_history else 0
    
    st.markdown(f'''
    <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
        <div style="background:#f5a623; padding:10px 20px; border-radius:10px;">
            <p style="margin:0; color:#2d5a27; font-weight:bold;">🏆 Score: {st.session_state.qa_score}/{len(st.session_state.qa_history)}</p>
        </div>
        <div style="background:rgba(255,255,255,0.2); padding:10px 20px; border-radius:10px;">
            <p style="margin:0; color:white; font-weight:bold;">Question {st.session_state.qa_index + 1} of {total_questions}</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.progress((st.session_state.qa_index + 1) / total_questions)
    
    st.markdown(f'''
    <div class="card">
        <span class="category-badge">{current_q["category"]}</span>
        <p style="color:#2d5a27; font-size:1.2rem; font-weight:bold; margin-top:15px; line-height:1.5;">{current_q["scenario"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if not st.session_state.qa_answered:
        for letter, text in current_q["options"].items():
            if st.button(f"{letter}) {text}", key=f"qa_opt_{letter}", use_container_width=True):
                st.session_state.qa_selected = letter
                st.session_state.qa_answered = True
                if letter == current_q["correct"]:
                    st.session_state.qa_score += 1
                st.session_state.qa_history.append({
                    "question": current_q["scenario"],
                    "selected": letter,
                    "correct": current_q["correct"],
                    "got_it": letter == current_q["correct"]
                })
                st.rerun()
    else:
        for letter, text in current_q["options"].items():
            if letter == current_q["correct"]:
                st.markdown(f'''
                <div style="background:#d4edda; padding:15px; border-radius:10px; margin:5px 0; border-left:5px solid #28a745;">
                    <p style="margin:0; color:#2d5a27;"><strong>✅ {letter}) {text}</strong></p>
                </div>
                ''', unsafe_allow_html=True)
            elif letter == st.session_state.qa_selected:
                st.markdown(f'''
                <div style="background:#f8d7da; padding:15px; border-radius:10px; margin:5px 0; border-left:5px solid #dc3545;">
                    <p style="margin:0; color:#721c24;"><strong>❌ {letter}) {text}</strong></p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div style="background:#e9ecef; padding:15px; border-radius:10px; margin:5px 0;">
                    <p style="margin:0; color:#6c757d;">{letter}) {text}</p>
                </div>
                ''', unsafe_allow_html=True)
        
        if st.session_state.qa_selected == current_q["correct"]:
            st.markdown(f'''
            <div class="card" style="background: linear-gradient(135deg, #d4edda, #c3e6cb); border-top: 5px solid #28a745;">
                <h4 style="color:#155724; margin-bottom:10px;">🎉 Correct!</h4>
                <p style="color:#155724; margin:0;">{current_q["explanation"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="card" style="background: linear-gradient(135deg, #f8d7da, #f5c6cb); border-top: 5px solid #dc3545;">
                <h4 style="color:#721c24; margin-bottom:10px;">Not quite!</h4>
                <p style="color:#721c24; margin:0;">{current_q["explanation"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.qa_index < total_questions - 1:
                if st.button("➡️ Next Question", use_container_width=True):
                    st.session_state.qa_index += 1
                    st.session_state.qa_answered = False
                    st.session_state.qa_selected = None
                    st.rerun()
            else:
                if st.button("🏆 See Final Score", use_container_width=True):
                    st.session_state.qa_show_final = True
                    st.rerun()
        with col2:
            if st.button("🔁 Start Over", use_container_width=True):
                st.session_state.qa_index = 0
                st.session_state.qa_score = 0
                st.session_state.qa_answered = False
                st.session_state.qa_selected = None
                st.session_state.qa_history = []
                st.session_state.qa_show_final = False
                st.rerun()
    
    if 'qa_show_final' not in st.session_state:
        st.session_state.qa_show_final = False
    
    if st.session_state.qa_show_final and len(st.session_state.qa_history) == total_questions:
        final_pct = (st.session_state.qa_score / total_questions) * 100
        if final_pct >= 90:
            grade = "QA Superstar!"
            grade_color = "#28a745"
            spriggle_emoji = "🎓"
            spriggle_message = "Spriggle is SO proud of you! You're a QA master!"
        elif final_pct >= 75:
            grade = "Solid Performance!"
            grade_color = "#4a9c3d"
            spriggle_emoji = "😊"
            spriggle_message = "Spriggle gives you a thumbs up! Great work!"
        elif final_pct >= 60:
            grade = "Keep Studying!"
            grade_color = "#f5a623"
            spriggle_emoji = "📖"
            spriggle_message = "Spriggle believes in you! A little more practice and you've got this!"
        else:
            grade = "Time to Review!"
            grade_color = "#dc3545"
            spriggle_emoji = "💪"
            spriggle_message = "Spriggle says don't give up! Review the guide and try again!"
        
        st.markdown(f'''
        <div class="card" style="text-align:center; border-top:6px solid {grade_color};">
            <p style="font-size:5rem; margin:0;">{spriggle_emoji}🌱</p>
            <h2 style="color:{grade_color}; margin:10px 0;">{grade}</h2>
            <p style="font-size:3rem; color:#2d5a27; font-weight:bold; margin:20px 0;">{st.session_state.qa_score} / {total_questions}</p>
            <p style="font-size:1.5rem; color:#666;">({final_pct:.0f}%)</p>
            <p style="color:#4a9c3d; font-style:italic; margin-top:15px;">{spriggle_message}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("### 📋 Question Review")
        for i, h in enumerate(st.session_state.qa_history):
            icon = "✅" if h["got_it"] else "❌"
            st.markdown(f"{icon} **Q{i+1}:** {h['question'][:50]}...")
        
        if st.button("🎮 Play Again", use_container_width=True):
            st.session_state.qa_index = 0
            st.session_state.qa_score = 0
            st.session_state.qa_answered = False
            st.session_state.qa_selected = None
            st.session_state.qa_history = []
            st.session_state.qa_show_final = False
            st.rerun()

with tab6:
    st.markdown('<p style="text-align:center;color:#e8f5e6;">Find answers fast — search or browse by category!</p>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search FAQs", placeholder="Type keywords like 'long grass' or 'payment'...")
    
    st.markdown("**Or browse by category:**")
    categories = ["All Categories"] + list(faq_data.keys())
    selected_faq_cat = st.selectbox("Select a category", categories, label_visibility="collapsed")
    
    def search_faqs(query):
        results = []
        query_lower = query.lower()
        for category, faqs in faq_data.items():
            for faq in faqs:
                if query_lower in faq["question"].lower() or query_lower in faq["answer"].lower() or query_lower in faq["phrasing"].lower():
                    results.append({"category": category, **faq})
        return results
    
    if search_query:
        results = search_faqs(search_query)
        if results:
            st.markdown(f'<p style="color:#e8f5e6;">Found {len(results)} result(s) for "{search_query}"</p>', unsafe_allow_html=True)
            for r in results:
                with st.expander(f"📌 {r['question']}"):
                    st.markdown(f'''
                    <div style="background:#e8f5e6; padding:10px; border-radius:8px; margin-bottom:10px;">
                        <p style="margin:0; color:#666; font-size:0.8rem;">Category: {r["category"]}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown(f"**📋 The Facts:**")
                    st.markdown(f"{r['answer']}")
                    st.markdown(f"**💬 How to say it (in your own words):**")
                    st.markdown(f'<div style="background:#fffef5; padding:15px; border-radius:10px; border-left:4px solid #4a9c3d;"><em>"{r["phrasing"]}"</em></div>', unsafe_allow_html=True)
        else:
            st.warning(f'No results found for "{search_query}". Try different keywords!')
    
    elif selected_faq_cat != "All Categories":
        faqs = faq_data[selected_faq_cat]
        st.markdown(f'<p style="color:#e8f5e6;">{len(faqs)} questions in {selected_faq_cat}</p>', unsafe_allow_html=True)
        for faq in faqs:
            with st.expander(f"📌 {faq['question']}"):
                st.markdown(f"**📋 The Facts:**")
                st.markdown(f"{faq['answer']}")
                st.markdown(f"**💬 How to say it (in your own words):**")
                st.markdown(f'<div style="background:#fffef5; padding:15px; border-radius:10px; border-left:4px solid #4a9c3d;"><em>"{faq["phrasing"]}"</em></div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<p style="color:#e8f5e6;">Browse all categories:</p>', unsafe_allow_html=True)
        for category, faqs in faq_data.items():
            st.markdown(f"### {category}")
            for faq in faqs:
                with st.expander(f"📌 {faq['question']}"):
                    st.markdown(f"**📋 The Facts:**")
                    st.markdown(f"{faq['answer']}")
                    st.markdown(f"**💬 How to say it (in your own words):**")
                    st.markdown(f'<div style="background:#fffef5; padding:15px; border-radius:10px; border-left:4px solid #4a9c3d;"><em>"{faq["phrasing"]}"</em></div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="card" style="background: linear-gradient(135deg, #f5a623, #f7b942); border-top: none; margin-top:20px;">
        <h4 style="color:#2d5a27; margin-bottom:10px;">💡 Remember</h4>
        <p style="color:#2d5a27; margin:0;">The phrasing examples are just guides — don't memorize them word-for-word! Use the key points and put them in YOUR voice so it sounds natural and conversational.</p>
    </div>
    ''', unsafe_allow_html=True)
