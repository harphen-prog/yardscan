import streamlit as st
import datetime

st.set_page_config(page_title="YardScan Pro - Virtual Landscaping Advice", page_icon="🌿", layout="wide")

# --- INIT ---
if "step" not in st.session_state: st.session_state.step = "signup"
if "pro" not in st.session_state: st.session_state.pro = False
if "data" not in st.session_state: st.session_state.data = {}

# --- HIDDEN BYPASS (No UI, only via invitation link) ---
params = st.query_params
invite = params.get("invite", "")
ref = params.get("ref", "")
if invite == "HARRYVIP" or ref:
    st.session_state.pro = True

# --- STEP 1: SIGN UP ---
if st.session_state.step == "signup":
    st.title("🌿 YardScan Pro")
    st.subheader("Virtual Landscaping Advice")
    st.write("Professional landscape guidance from your photos & address.")
    
    with st.form("signup"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        address = st.text_input("Property Address*")
        country = st.selectbox("Country", ["USA", "Canada", "Mexico"])
        submit = st.form_submit_button("Create My Account")
        
        if submit:
            if not name or not email or not address:
                st.error("Please fill all fields")
            else:
                st.session_state.data = {"name": name, "email": email, "address": address, "country": country}
                st.session_state.step = "agreement"
                st.rerun()
    st.stop()

# --- STEP 2: FULL AGREEMENT (AFTER SIGNUP, BEFORE APP) ---
if st.session_state.step == "agreement":
    st.title("Terms & Service Agreement")
    st.markdown(f"""
    **Welcome {st.session_state.data['name']}**

    **1. Nature of Service:** YardScan Pro provides VIRTUAL landscaping advice and estimates only. All measurements, plant diagnoses, and designs are AI-assisted estimates.

    **2. No On-Site Guarantee:** Recommendations must be verified on-site. We are not liable for costs, plant loss, or construction decisions.

    **3. Photos & Privacy:** Photos you submit are used only to generate your advice report.

    **4. Professional Advice:** This is educational guidance, not a substitute for licensed contractor or arborist inspection for major work.

    **5. Subscription Tiers:** Free tier includes measurement & basic advice. Pro tier includes complete design, flower beds, driveway & plant doctor.

    **6. Canada/Mexico:** Estimates adapt to local units and pricing but are still estimates.
    
    **By checking below, you agree to these terms.**
    """)
    agree = st.checkbox("I have read and AGREE to the Terms above")
    if st.button("Agree & Continue to My YardScan"):
        if agree:
            st.session_state.step = "scan"
            st.rerun()
        else:
            st.error("You must agree to continue")
    st.stop()

# --- STEP 3: SCAN REQUEST (CORE PRODUCT) ---
if st.session_state.step == "scan":
    st.title(f"Hello {st.session_state.data['name']} 👋")
    st.caption(f"Property: {st.session_state.data['address']} | {st.session_state.data['country']}")
    if st.session_state.pro: st.success("✅ PRO ACCESS via invitation")

    st.header("Step 1: Submit Your Property Scan")
    st.write("Enter address confirmed, now upload photos for analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        front = st.file_uploader("Front of house + yard", type=["jpg","png","jpeg"])
    with col2:
        backyard = st.file_uploader("Backyard / Problem areas", type=["jpg","png","jpeg"])

    if st.button("🚀 Generate My Virtual Advice Report", type="primary"):
        if not front:
            st.error("Please upload at least front yard photo")
        else:
            st.session_state.step = "results_free"
            st.rerun()
    st.stop()

# --- STEP 4: FREE TIER RESULT (Measurement + Basic Plant Advice) ---
if st.session_state.step == "results_free":
    st.title("📋 Your Virtual Landscaping Advice Report")
    st.subheader(f"For: {st.session_state.data['address']}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated Lawn Area", "2,450 sq ft")
    c2.metric("Usable Bed Space", "340 sq ft")
    c3.metric("Sun Exposure", "Full Sun - South")

    st.info("**Basic Plant Advice:** Your soil looks compacted near foundation. Add compost. Existing shrubs show overcrowding - consider thinning for air flow.")
    
    st.divider()
    st.header("Want a Complete Design?")
    st.write("We can now create: Suggested flower beds that match your house architecture, driveway update, and new plants that thrive in your zone.")
    
    if st.session_state.pro:
        if st.button("Unlock My Full Design (PRO Included) ➡️"):
            st.session_state.step = "pro_design"
            st.rerun()
    else:
        st.warning("Full design, flower beds, driveway & Plant Doctor are PRO features.")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Upgrade to Pro - View Design"):
                st.session_state.step = "pro_design"
                st.rerun()
        with col_b:
            st.caption("Or use your invitation link: yardscanpro.com/?invite=HARRYVIP")

    if st.button("← Start New Scan"): 
        st.session_state.step = "scan"
        st.rerun()
    st.stop()

# --- STEP 5: PRO DESIGN (Byproducts now) ---
if st.session_state.step == "pro_design":
    if not st.session_state.pro:
        st.warning("🔒 This is a Pro feature. Please upgrade or use invitation link.")
        if st.button("Back to Free Report"):
            st.session_state.step = "results_free"
            st.rerun()
        st.stop()

    st.title("✨ Complete Landscape Design - PRO")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌷 Flower Beds by Architecture", "🚗 Driveway Update", "🌱 New Plant Suggestions", "🩺 Plant Doctor + Recognition"])

    with tab1:
        st.subheader("Flower Beds Matching Your House Architecture")
        st.write(f"House style detected: Colonial / Brick - recommending Allium Millenium for structure + Zinnia for color")
        st.success("Design: Curved bed along walkway, 12x Allium Millenium (pollinator magnet), 20x Zinnia mix, mulch 3 inches")

    with tab2:
        st.subheader("Driveway / Paver Update")
        st.slider("New Width", 10, 24, 12)
        st.metric("Estimated Pro Install", "$4,800 - $6,200")

    with tab3:
        st.subheader("New Plants That Match Architecture")
        st.write("Suggested: Boxwood hedge for formal look, Hydrangea for shade corner, Allium for seasonal color")

    with tab4:
        st.subheader("Plant Analysis & Treatment")
        sick = st.file_uploader("Upload sick plant for diagnosis", key="sick2")
        if sick:
            st.image(sick, width=300)
            if st.button("Analyze & Treat"):
                st.error("Diagnosis: Fungal leaf spot. Treatment: Remove leaves, neem oil spray, improve drainage.")
    
    st.divider()
    if st.button("Download Full Report PDF (Coming Tomorrow with Voice)"):
        st.balloons()

st.caption(f"YardScan Pro Virtual Advice © {datetime.datetime.now().year}")
