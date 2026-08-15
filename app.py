import streamlit as st
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

# --- SESSION STATE ---
if "agreed" not in st.session_state: st.session_state.agreed = False
if "first_name" not in st.session_state: st.session_state.first_name = ""
if "pro_unlocked" not in st.session_state: st.session_state.pro_unlocked = False

# --- 1. LEGAL GATE (MUST BE FIRST) ---
if not st.session_state.agreed:
    st.title("🌿 YardScan Pro - Terms")
    st.markdown("""
    **DISCLAIMER:** YardScan Pro is an estimation and educational tool only.
    Measurements, diagnoses, and cost estimates are AI-assisted and should be verified on-site.
    Not a substitute for professional landscaping advice.
    """)
    agree = st.checkbox("I AGREE to Terms and Conditions")
    if st.button("Continue to YardScan Pro"):
        if agree:
            st.session_state.agreed = True
            st.rerun()
        else:
            st.error("You must agree to continue")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    st.session_state.first_name = st.text_input("First Name", st.session_state.first_name)
    
    country = st.selectbox("Country", ["USA", "Canada", "Mexico"])
    if country == "Canada":
        st.caption("🇨🇦 French support: Bonjour! Measurements in sq ft / sq m")
    elif country == "Mexico":
        st.caption("🇲🇽 Soporte en Español activado")
    
    st.divider()
    st.subheader("🔑 Pro Access")
    bypass = st.text_input("Bypass Code / Referral", type="password")
    if bypass == "HARRYVIP":
        st.session_state.pro_unlocked = True
        st.success("✅ 30 Days Free Pro Unlocked!")
    if "ref=" in bypass or len(bypass) > 5:
        st.info(f"Referral tracked: {bypass}")

    if st.session_state.pro_unlocked:
        st.success("PRO VERSION ACTIVE")
    else:
        st.warning("Free Version - Upgrade with HARRYVIP")

# --- MAIN APP ---
name = st.session_state.first_name or "there"
st.title(f"Hey {name}, welcome to YardScan Pro 🌸")

tab1, tab2, tab3, tab4 = st.tabs(["📏 Measure Property", "🌷 Flower Beds", "🚗 Driveway / Pavers", "🩺 Plant Doctor"])

with tab1:
    st.subheader("Property Measurement")
    st.write("Upload aerial / property photo for AI measurement.")
    uploaded = st.file_uploader("Upload property image", type=["jpg","png","jpeg"])
    if uploaded:
        st.image(uploaded, caption="Property")
        st.metric("Estimated Lawn Area", "2,450 sq ft" if country=="USA" else "228 m²")
        st.metric("Estimated Mulch Needed", "8 cubic yards")

with tab2:
    st.subheader("Flower Bed Designer")
    st.write("Design with Allium Millenium, Zinnias, etc.")
    bed_style = st.selectbox("Flower Type", ["Allium Millenium (Pollinator Magnet)", "Zinnia Mix", "Custom"])
    if st.button("Generate Design"):
        st.success(f"Design created for {bed_style} - Pollinator friendly layout ready!")

with tab3:
    st.subheader("Driveway & Paver Estimator")
    length = st.slider("Length (ft)", 10, 100, 40)
    width = st.slider("Width (ft)", 8, 30, 12)
    cost = length * width * 12
    st.metric("Estimated Cost", f"${cost:,} USD")
    if country != "USA":
        st.metric("Local Estimate", f"${cost*1.35:,.0f} CAD" if country=="Canada" else f"${cost*18:,.0f} MXN")

with tab4:
    st.subheader("Plant Doctor - Diagnose")
    plant_pic = st.file_uploader("Upload sick plant photo", type=["jpg","png"], key="plant")
    if plant_pic:
        st.image(plant_pic, width=300)
        if st.button("Diagnose"):
            st.warning("Diagnosis: Possible overwatering + fungal spot. Remove affected leaves, improve drainage.")
            st.info("Care Tip for Allium Millenium: Full sun, well-drained soil, drought tolerant once established.")

st.divider()
st.caption(f"YardScan Pro © {datetime.datetime.now().year} | Referral: yardscanpro.com/?ref=HARRY123 | Support: Pro Call Agent coming tomorrow")
