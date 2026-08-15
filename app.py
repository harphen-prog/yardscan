import streamlit as st
import datetime, random, io
from PIL import Image

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

if "step" not in st.session_state: st.session_state.step = "start"
if "pro" not in st.session_state: st.session_state.pro = False
if "user" not in st.session_state: st.session_state.user = {}
if "approval_code" not in st.session_state: st.session_state.approval_code = str(random.randint(100000,999999))

# Hidden invite bypass - no UI
params = st.query_params
if params.get("invite") == "HARRYVIP" or params.get("ref"):
    st.session_state.pro = True

# --- START: Name & Email - Home Address ---
if st.session_state.step == "start":
    st.title("🌿 - Yard Scan -")
    st.subheader("Start → Name & Email - Home address")
    with st.form("start_form"):
        email = st.text_input("Email* (will be your username)")
        home_address = st.text_input("Home Address*")
        password = st.text_input("Choose a Password*", type="password")
        c = st.form_submit_button("Continue")
        if c:
            if not email or not home_address or not password:
                st.error("Fill all fields")
            else:
                st.session_state.user = {"email": email, "username": email, "address": home_address, "password": password}
                st.session_state.step = "agree"
                st.rerun()
    st.stop()

# --- AGREE WITH TERMS ---
if st.session_state.step == "agree":
    st.title("Agree with terms")
    st.markdown(f"""
    **User: {st.session_state.user['username']}**
    YardScan Pro is a VIRTUAL landscaping advice service. All propositions are AI-assisted estimates. You must verify on-site. We are not liable for costs or plant loss.
    Photos are used only for your report. Free tier includes analysis + PDF. Paid tier includes architectural design + realistic render + video how-to + voice assistant.
    """)
    agree = st.checkbox("I AGREE")
    if st.button("Generate Approval Code"):
        if agree:
            st.session_state.step = "approval"
            st.rerun()
        else:
            st.error("Must agree")
    st.stop()

# --- APPROVAL CODE IN EMAIL ---
if st.session_state.step == "approval":
    st.title("Approval Code sent to email")
    st.info(f"Demo Code (in production, emailed to {st.session_state.user['email']}): **{st.session_state.approval_code}**")
    code = st.text_input("Enter Approval Code to access App")
    if st.button("Access Free Tier"):
        if code == st.session_state.approval_code or code == "HARRYVIP":
            st.session_state.step = "free"
            if code == "HARRYVIP": st.session_state.pro = True
            st.rerun()
        else:
            st.error("Wrong code")
    st.stop()

# --- FREE TIER ---
if st.session_state.step == "free":
    st.title("✅ Access to Free Tier Given")
    st.caption(f"{st.session_state.user['username']} | {st.session_state.user['address']}")
    if st.session_state.pro: st.success("PRO invitation active")

    tab1, tab2 = st.tabs(["1. Photo Analysis + Propositions", "2. Plant Scanner"])

    with tab1:
        st.subheader("Free Tier Content 1: Photo Taken or Submitted")
        photo = st.file_uploader("Take or submit home/yard photo", type=["jpg","png","jpeg"])
        if photo:
            st.image(photo, caption="Submitted Photo", width=400)
            if st.button("Analyze Picture & Propose"):
                st.session_state["analysis_done"] = True
        
        if st.session_state.get("analysis_done"):
            st.divider()
            st.subheader("📋 Comprehensive Written Proposition")
            st.markdown("""
            **Analysis:**
            - Blind spot detected: Left side of entryway empty, low curb appeal.
            - Existing plants: Overcrowded boxwood near foundation.
            
            **Propositions:**
            - Replace 2 boxwood with Allium Millenium (Zone 5-8, pollinator magnet, architectural height 20").
            - Add curved flower bed along walkway: 12x Zinnia + 3x Hydrangea (zone-matched).
            - Mulch recommendation: 3" hardwood.
            
            **Affiliate Links (display at end):**
            - [Allium Millenium - Amazon](https://amazon.com) | [Zinnia Seeds - Home Depot]
            """)
            st.download_button("📄 Download Proposition as PDF (Comprehensive)", data="YardScan Free Report PDF Content Here", file_name="YardScan_Free_Proposition.pdf")

            st.warning("Want more? Invitation to upgrade to Paid tier for more features ↓")
            if st.button("Upgrade to Paid Tier →"):
                st.session_state.step = "paid_collect"
                st.rerun()

    with tab2:
        st.subheader("Free Tier Content 2: Plant Scanner")
        sick = st.file_uploader("Upload plant to identify sickness", type=["jpg","png"], key="sick")
        if sick:
            st.image(sick, width=300)
            if st.button("Identify & Propose Solution"):
                st.write("**Identification:** Hosta - Fungal leaf spot detected")
                st.write("**Solution (written):** Remove affected leaves, improve air circulation, apply neem oil, avoid overhead watering.")
                st.download_button("Download Solution PDF", data="Plant solution", file_name="Plant_Solution.pdf", key="pdf2")

    st.stop()

# --- PAID TIER COLLECT ---
if st.session_state.step == "paid_collect":
    st.title("⭐ Paid Option")
    st.write("Collect Client Full Name, Phone Number + Everything Tier 1 Plus")
    with st.form("paid_form"):
        full_name = st.text_input("Full Name*")
        phone = st.text_input("Phone Number*")
        zone = st.selectbox("Your Hardiness Zone", ["Zone 5", "Zone 6", "Zone 7", "Zone 8", "Zone 9"])
        submit = st.form_submit_button("Unlock Paid Features")
        if submit:
            st.session_state.user.update({"full_name": full_name, "phone": phone, "zone": zone})
            if full_name and phone:
                st.session_state.pro = True
                st.session_state.step = "paid_features"
                st.rerun()
            else:
                st.error("Full name & phone required")
    st.stop()

# --- PAID FEATURES ---
if st.session_state.step == "paid_features":
    st.title("🏡 Paid Tier - Architectural Garden Design")
    st.success(f"Welcome {st.session_state.user.get('full_name')} | {st.session_state.user.get('zone')}")
    
    t1, t2, t3, t4 = st.tabs(["Flower Beds + Zone Plants", "Realistic Picture", "Plant Analysis + Video", "Voice Assistant"])
    
    with t1:
        st.subheader("Architectural Garden Design For Flower beds with Proposed Plants in regard to the zone")
        st.write(f"For {st.session_state.user['zone']}: Colonial architecture → Formal curved beds")
        st.success("Proposed: 12x Allium Millenium (Zone 5-8), 20x Zinnia Profusion, 3x Boxwood Wintergreen - Matched to house color")

    with t2:
        st.subheader("Realistic Picture of the Proposed based on exact user home picture")
        st.info("This render will be based on the exact home picture submitted in Tier 1")
        st.image("https://images.unsplash.com/photo-1558618666-fcd25c85cd64", caption="AI Render Preview - Your house with new beds (Tomorrow: uses your actual photo)")
        if st.button("Generate My Realistic Render"):
            st.balloons()
            st.write("Rendering... (In final version, generates photorealistic proposal)")

    with t3:
        st.subheader("Plants Analysis come with short video - how to")
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.write("How to plant Allium Millenium: Full sun, well-drained, plant 4in deep in fall.")

    with t4:
        st.subheader("Access to interactive voice assistant")
        st.warning("Voice clone coming tomorrow - placeholder ready")
        st.chat_input("Ask your garden voice assistant...")

    st.divider()
    st.download_button("📄 Download COMPLETE Paid Proposition PDF", data="Complete Paid Report", file_name="YardScan_Paid_Complete.pdf")

st.caption(f"YardScan Pro © {datetime.datetime.now().year}")
