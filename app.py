import streamlit as st
import json, os
from PIL import Image
import datetime

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

# === PREMIUM CSS DESIGN ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* {font-family: 'Inter', sans-serif;}
.main {background: #f8faf8;}
h1 {font-weight: 800!important; letter-spacing: -1.5px;}
.hero {
  background: linear-gradient(135deg, #0f5c36 0%, #22c55e 100%);
  padding: 40px; border-radius: 20px; color: white; margin-bottom: 25px;
}
.card {
  background: white; border-radius: 16px; padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #eef2ee;
  margin-bottom: 15px; transition: 0.3s;
}
.card:hover {transform: translateY(-3px); box-shadow: 0 12px 30px rgba(0,0,0,0.1);}
.badge {background:#dcfce7; color:#166534; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;}
.badge-red {background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:20px; font-size:12px;}
.price-tag {font-size:28px; font-weight:800; color:#0f5c36;}
</style>
""", unsafe_allow_html=True)

ADMIN_EMAIL = "harphen-prog@gmail.com"
STRIPE_LINK = "https://buy.stripe.com/test_00g5kL2V0"
AFF_FILE = "affiliates.json"

if os.path.exists(AFF_FILE):
    with open(AFF_FILE) as f: AFF = json.load(f)
else:
    AFF = {"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood","Black-Eyed Susan":"https://amazon.com/s?k=black+eyed+susan","Hydrangea":"https://amazon.com/s?k=hydrangea"}

if "users" not in st.session_state: st.session_state.users = {ADMIN_EMAIL: {"pw":"admin123","plan":"paid","role":"admin"}}
if "login" not in st.session_state: st.session_state.login=None
if "unlocked" not in st.session_state: st.session_state.unlocked=False
def is_admin(): return st.session_state.login and st.session_state.users.get(st.session_state.login,{}).get("role")=="admin"

with st.sidebar:
    st.markdown("## 🌿 YardScan Pro")
    st.caption("AI Landscape Designer v2.0")
    if st.session_state.login:
        st.success(f"👋 {st.session_state.login}")
        u=st.session_state.users[st.session_state.login]
        st.markdown(f"<span class='badge'>{u['plan'].upper()} PLAN</span>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True): st.session_state.login=None; st.session_state.unlocked=False; st.rerun()
        if is_admin():
            st.divider()
            st.markdown("### 🔧 Admin Back-Office")
            st.caption("Your affiliate links = Your commission")
            txt=st.text_area("Links JSON", json.dumps(AFF,indent=2), height=250)
            if st.button("💾 Save Links", type="primary", use_container_width=True):
                with open(AFF_FILE,"w") as f: f.write(txt); st.success("Saved!"); st.rerun()
    else:
        t1,t2=st.tabs(["Login","Sign Up Free"])
        with t1:
            e=st.text_input("Email"); p=st.text_input("Password", type="password")
            if st.button("Login", type="primary", use_container_width=True):
                if e in st.session_state.users and st.session_state.users[e]["pw"]==p:
                    st.session_state.login=e
                    if st.session_state.users[e]["plan"]=="paid": st.session_state.unlocked=True
                    st.rerun()
                else: st.error(f"Try {ADMIN_EMAIL} / admin123")
        with t2:
            ne=st.text_input("New Email", key="ne"); np=st.text_input("New Password", type="password", key="np")
            if st.button("Create Free Account", use_container_width=True):
                st.session_state.users[ne]={"pw":np,"plan":"free","role":"user"}; st.success("Created! Go to Login")

if not st.session_state.login:
    st.markdown('<div class="hero"><h1 style="color:white; margin:0;">AI Garden Designer That Sells Plants For You</h1><p style="opacity:0.9; font-size:18px; margin-top:10px;">Upload a yard photo → Get removal plan + new design + AI before/after + shopping links that pay YOU</p></div>', unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown('<div class="card"><h3>🌸 Comprehensive</h3><p>Not just plants. Full esthetics + effectiveness + removal + soil + maintenance analysis.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>💰 Monetized</h3><p>Every plant has YOUR affiliate link. $49/report + 8-12% on plants. You keep 100%.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><h3>🤖 AI Visual</h3><p>Client sees their exact house with new garden photoshopped. Instant YES.</p></div>', unsafe_allow_html=True)
    st.warning("👈 Login from sidebar to start - Free account works")
    st.stop()

plan=st.session_state.users[st.session_state.login]["plan"]
paid=plan=="paid" or st.session_state.unlocked

st.markdown(f'<div class="hero"><h2 style="color:white; margin:0;">Welcome back, {st.session_state.login.split("@")[0]}! 🌿</h2><p>Zip-based native plants • Professional report • Client-ready</p></div>', unsafe_allow_html=True)

c1,c2=st.columns([3,1])
with c1:
    zipc=st.text_input("📍 Client Zip Code", "19426")
    ups=st.file_uploader("📸 Upload 1-4 Yard Photos (Front yard = best for AI recreation)", accept_multiple_files=True, type=["jpg","jpeg","png"])
with c2:
    if not paid:
        st.markdown('<div class="card" style="border:2px solid #22c55e;"><h3>🔓 Unlock Full Report</h3><p>Free = 1 plant preview<br>Paid = Full removal + AI visual + 4 plants + Buy links</p></div>', unsafe_allow_html=True)
        st.link_button("Unlock for $49 →", STRIPE_LINK, type="primary", use_container_width=True)
        if st.button("✅ I Paid - Unlock", use_container_width=True): st.session_state.unlocked=True; st.rerun()
    else:
        st.markdown('<div class="card" style="background:#dcfce7;"><h3>✅ Paid Access</h3><p>Full report unlocked</p></div>', unsafe_allow_html=True)

if ups and st.button("✨ Generate Comprehensive Report", type="primary", use_container_width=True):
    st.balloons()
    st.markdown(f"## 📋 Comprehensive Landscape Report - Zone 7a • {zipc}")
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>1. Existing Analysis & Removal Plan</h3></div>', unsafe_allow_html=True)
        if paid:
            st.markdown('<div class="card"><span class="badge-red">REMOVE</span> <b>Overgrown Juniper (Front window)</b><br>Blocks light, 70s look, root too close to foundation. <i>Cost: $150 removal</i></div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><span class="badge-red">REMOVE</span> <b>Diseased Boxwood (Corner)</b><br>Leaf blight - will infect new plants if kept.</div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><span class="badge">KEEP</span> <b>Mature Maple</b><br>Excellent shade value, anchor tree.</div>', unsafe_allow_html=True)
        else: st.info("🔒 Paid: See removal/keep/relocate plan")
    with c2:
        st.image(ups[0], caption="Original")
        if paid: st.image(ups[0], caption="✨ AI PROPOSED: Same house, lavender border + boxwood hedge + hydrangea corner (Photorealistic in production with OpenAI)")

    st.divider()
    st.markdown("### 2. New Design - Plants & Flowers")
    plants=[
        {"name":"Lavender","why":"Purple aesthetic, fragrant, pollinator, drought proof","sun":"Full Sun","water":"Low","price":"$14.99"},
        {"name":"Boxwood","why":"Evergreen structure year-round","sun":"Part Sun","water":"Med","price":"$29.99"},
        {"name":"Black-Eyed Susan","why":"Native PA, blooms 4 months, zero care","sun":"Full Sun","water":"Low","price":"$11.99"},
        {"name":"Hydrangea","why":"High impact blooms, shade corner","sun":"Part Shade","water":"Med","price":"$34.99"},
    ]
    cols=st.columns(2)
    for i,pl in enumerate(plants):
        with cols[i%2]:
            if paid:
                st.markdown(f'<div class="card"><h4>{pl["name"]}</h4><p style="color:#666; font-size:14px;">{pl["why"]}</p><p>☀️ {pl["sun"]} | 💧 {pl["water"]}</p><p class="price-tag">{pl["price"]}</p></div>', unsafe_allow_html=True)
                st.link_button(f"🛒 Buy {pl['name']}", AFF.get(pl['name'],"#"), use_container_width=True)
            else:
                if i==0: st.markdown(f'<div class="card"><h4>{pl["name"]} (Preview)</h4><p>{pl["why"]}</p><p>🔒 Other 3 plants + buy links = Paid</p></div>', unsafe_allow_html=True)
