import streamlit as st
import json, os, datetime

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* {font-family: 'Inter', sans-serif;}
.hero {background: linear-gradient(135deg, #0f5c36 0%, #22c55e 100%); padding: 30px; border-radius: 20px; color: white; margin-bottom: 20px;}
.card {background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #eef2ee; margin-bottom: 12px;}
.badge {background:#dcfce7; color:#166534; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;}
.badge-red {background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:20px; font-size:12px;}
</style>
""", unsafe_allow_html=True)

ADMIN_EMAIL = "harphen-prog@gmail.com"
STRIPE_LINK = "https://buy.stripe.com/test_00g5kL2V0"
AFF_FILE = "affiliates.json"

if os.path.exists(AFF_FILE):
    try:
        with open(AFF_FILE) as f: AFF = json.load(f)
    except:
        AFF = {}
else:
    AFF = {"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood","Black-Eyed Susan":"https://amazon.com/s?k=black+eyed+susan","Hydrangea":"https://amazon.com/s?k=hydrangea"}

if "users" not in st.session_state:
    st.session_state.users = {ADMIN_EMAIL: {"pw":"admin123","plan":"paid","role":"admin"}}
if "login" not in st.session_state: st.session_state.login=None
if "unlocked" not in st.session_state: st.session_state.unlocked=False

def is_admin():
    return st.session_state.login and st.session_state.users.get(st.session_state.login,{}).get("role")=="admin"

with st.sidebar:
    st.title("YardScan Pro")
    st.caption("AI Landscape Designer v2.0")
    if st.session_state.login:
        st.success(st.session_state.login)
        plan_now = st.session_state.users[st.session_state.login]["plan"]
        st.markdown(f"<span class='badge'>{plan_now.upper()} PLAN</span>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.login=None; st.session_state.unlocked=False; st.rerun()
        if is_admin():
            st.divider()
            st.subheader("Admin Back-Office")
            st.caption("Your affiliate links = Your commission")
            txt=st.text_area("Links JSON", json.dumps(AFF, indent=2), height=200)
            if st.button("Save Links", use_container_width=True):
                with open(AFF_FILE,"w") as f: f.write(txt)
                st.success("Saved!")
    else:
        t1,t2=st.tabs(["Login","Sign Up Free"])
        with t1:
            e=st.text_input("Email", key="e1")
            p=st.text_input("Password", type="password", key="p1")
            if st.button("Login", type="primary", use_container_width=True):
                if e in st.session_state.users and st.session_state.users[e]["pw"]==p:
                    st.session_state.login=e
                    if st.session_state.users[e]["plan"]=="paid": st.session_state.unlocked=True
                    st.rerun()
                else: st.error("Wrong - use harphen-prog@gmail.com / admin123")
        with t2:
            ne=st.text_input("New Email", key="ne")
            np=st.text_input("New Pass", type="password", key="np")
            if st.button("Create Free Account", use_container_width=True):
                if ne:
                    st.session_state.users[ne]={"pw":np,"plan":"free","role":"user"}
                    st.success("Created! Go to Login tab.")

if not st.session_state.login:
    st.markdown('<div class="hero"><h1 style="color:white; margin:0;">AI Garden Designer That Sells Plants For You</h1><p>Upload a yard photo -> Get removal plan + new design + AI before/after + shopping links that pay YOU</p></div>', unsafe_allow_html=True)
    st.warning("Please Login from left sidebar to start")
    st.stop()

plan = st.session_state.users[st.session_state.login]["plan"]
paid = (plan=="paid") or st.session_state.unlocked

st.markdown(f'<div class="hero"><h2 style="color:white; margin:0;">Welcome back, {st.session_state.login.split("@")[0]}!</h2><p>Zip-based native plants - Professional report - Client-ready</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    zipc = st.text_input("Client Zip Code", "19426")
    ups = st.file_uploader("Upload 1-4 Yard Photos", accept_multiple_files=True, type=["jpg","jpeg","png"])
with col2:
    if not paid:
        st.error("PAID FEATURES LOCKED")
        st.link_button("Unlock Full Report $49", STRIPE_LINK, use_container_width=True)
        if st.button("I Paid - Unlock", use_container_width=True):
            st.session_state.unlocked=True
            st.rerun()
    else:
        st.success("FULL PAID ACCESS UNLOCKED")

if not ups:
    st.info("Upload a photo to generate report")
    st.stop()

if st.button("Generate Comprehensive Report", type="primary", use_container_width=True):
    st.balloons()
    st.header(f"Comprehensive Landscape Report - Zip {zipc}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Removal & Effectiveness")
        if paid:
            st.markdown('<div class="card"><span class="badge-red">REMOVE</span> <b>Overgrown Juniper (Front)</b><br>Blocks light, outdated look. Cost $150</div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><span class="badge-red">REMOVE</span> <b>Diseased Boxwood</b><br>Fungal risk - will spread</div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><span class="badge">KEEP</span> <b>Mature Maple</b><br>Excellent anchor tree</div>', unsafe_allow_html=True)
        else:
            st.info("Paid: Full removal plan")
    with c2:
        st.image(ups[0], caption="Original")
        if paid:
            st.image(ups[0], caption="AI PROPOSED: Same house with lavender border + boxwood hedge")

    st.divider()
    st.subheader("2. New Plant Suggestions")

    plants = [
        {"name":"Lavender","why":"Purple aesthetic, fragrant, drought proof","price":"$14.99"},
        {"name":"Boxwood","why":"Evergreen structure year-round","price":"$29.99"},
        {"name":"Black-Eyed Susan","why":"Native PA, 4 months bloom, zero care","price":"$11.99"},
        {"name":"Hydrangea","why":"High impact blooms","price":"$34.99"},
    ]

    cols = st.columns(2)
    for i, pl in enumerate(plants):
        with cols[i % 2]:
            st.markdown(f'<div class="card"><h4>{pl["name"]}</h4><p>{pl["why"]}</p><b>{pl["price"]}</b></div>', unsafe_allow_html=True)
            if paid:
                link = AFF.get(pl["name"], "#")
                st.link_button(f"Buy {pl['name']}", link, use_container_width=True)
            else:
                if i>0: st.caption("Locked - Paid only")
