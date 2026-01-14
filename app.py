import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="The Cutting Edge", page_icon="🌱", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #2d5a27 0%, #4a9c3d 50%, #3d8a35 100%); }
    .main-header { text-align: center; color: white; padding: 20px 0; }
    .main-header h1 { color: #fffef5; font-size: 2.5rem; margin-bottom: 0; }
    .main-header .highlight { color: #f5a623; }
    .main-header p { color: #e8f5e6; }
    .card { background: #fffef5; border-radius: 20px; padding: 25px; margin: 15px 0; border-top: 6px solid #4a9c3d; }
    .category-badge { background: #4a9c3d; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 15px; }
    .surface-text { color: #666; font-style: italic; padding: 10px 0; border-bottom: 2px dashed #ddd; margin-bottom: 15px; }
    .reason-label { color: #f5a623; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
    .reason-text { color: #2d5a27; font-size: 1.3rem; font-weight: bold; line-height: 1.4; }
    .approach-label { color: #4a9c3d; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
    .approach-text { color: #2d5a27; font-size: 1.1rem; line-height: 1.6; }
    .success-box { background: #d4edda; border-radius: 10px; padding: 15px; text-align: center; color: #2d5a27; font-weight: bold; }
    div[data-testid="stHorizontalBlock"] button { background: linear-gradient(135deg, #6bc75f, #4a9c3d); color: white; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Flashcard data
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

SCRIPT_URL = "https://script.google.com/a/macros/lawnstarter.com/s/AKfycbyEGIP63SoZrL5XAAzfpY7NfaThcMIf_R36_YebHHsRkIeUWGfCmzVRHxI1OVs_WFNv/exec"

# Header
st.markdown('<div class="main-header"><h1>🌱 The <span class="highlight">Cutting Edge</span></h1></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["📚 Flashcards", "📉 Loss Tracker"])

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
            params = urllib.parse.urlencode({
                "agentName": agent_name,
                "agentId": agent_id,
                "disposition": disposition,
                "timestamp": timestamp
            })
            full_url = f"{SCRIPT_URL}?{params}"
            st.markdown(f'<div class="success-box">✓ Logged: {disposition}</div>', unsafe_allow_html=True)
            st.markdown(f'<a href="{full_url}" target="_blank"><button style="width:100%;padding:10px;margin-top:10px;background:#4a9c3d;color:white;border:none;border-radius:10px;font-weight:bold;cursor:pointer;">Click here to send to Google Sheet</button></a>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)
