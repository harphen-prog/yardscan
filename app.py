import streamlit as st
import datetime, random

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- HIDE ALL STREAMLIT ICONS / FORK / HOSTED BADGE ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stToolbar"] {visibility: hidden!important;}
div[data-testid="stStatusWidget"] {visibility: hidden;}
a[href^="https://github.com"] {display: none!important;}
button[kind="header"] {display: none!important;}
</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state.step = "auth"
if "pro" not in st.session_state: st.session_state.pro = False
if "users_db" not in st.session_state: st.session_state.users_db = {}
if "user" not in st.session_state: st.session_state.user = {}
if "approval_code" not in st.session_state: st.session_state.approval_code = str(random.randint(100000,999999))

params = st.query_params
if params.get("invite") == "HARRYVIP" or params.get("ref"):
    st.session_state.pro = True

# --- AUTH WITH 2 BUTTONS ---
if st.session_state.step == "auth":
    st.title("🌿 YardScan Pro")
    st.write("Virtual Landscaping Advice")

    email = st.text_input("Email* (will be your username)")
    home = st.text_input("Home Address*")
    pwd = st.text_input("Choose a Password*", type="password")

    # 2 BUTTONS YOU ASKED FOR
    col1, col2 = st.columns(2)
    with col1:
        create = st.button("Create Account", type="primary", use_container_width=True)
    with col2:
        signin = st.button("Sign In", use_container_width=True)

    if create:
        if not email or not home or not pwd:
            st.error("Fill all fields")
        else:
            st.session_state.users_db[email] = {"email": email, "username": email, "address": home, "password": pwd}
            st.session_state.user = st.session_state.users_db[email]
            st.session_state.step = "agreement"
            st.rerun()

    if signin:
        u = st.session_state.users_db.get(email)
        if u and u["password"] == pwd:
            st.session_state.user = u
            st.session_state.step = "free"
            st.rerun()
        else:
            st.error("Wrong email/password or account not created yet. Click Create Account first.")

    st.stop()

# --- AGREEMENT ---
if st.session_state.step == "agreement":
    st.title("Terms & Agreement")
    st.write(f"User {st.session_state.user['username']} generated as email")
    agree = st.checkbox("Agree with terms")
    if st.button("Generate Approval Code in email"):
        if agree:
            st.session_state.step = "approval"
            st.rerun()
    st.stop()

# --- APPROVAL ---
if st.session_state.step == "approval":
    st.info(f"Demo code: {st.session_state.approval_code}")
    code = st.text_input("Enter Approval Code")
    if st.button("Access Free Tier"):
        if code == st.session_state.approval_code or code == "HARRYVIP":
            st.session_state.step = "free"
            st.rerun()
    st.stop()

# --- FREE TIER (your handwritten flow) ---
if st.session_state.step == "free":
    st.title("Free Tier")
    st.write(f"Access to Free tier Given for {st.session_state.user['username']}")
    photo = st.file_uploader("Photo Taken or Submitted")
    if photo and st.button("Analyze"):
        st.write("Analysis: Blind spots identified, propose new plants. Affiliate links at end. PDF download comprehensive.")
        st.download_button("Download PDF", b"pdf", "report.pdf")
        if st.button("Upgrade to Paid"): st.session_state.step = "paid"; st.rerun()
    st.stop()

if st.session_state.step == "paid":
    st.title("Paid Tier")
    st.write("Architectural Garden design + Realistic picture from Tier 1 photo + Video how-to + Voice")
    st.stop()
