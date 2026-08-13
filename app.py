import streamlit as st, json, os, datetime, base64
from pathlib import Path

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* {font-family: 'Inter', sans-serif;}
.hero {background: linear-gradient(135deg, #0f5c36 0%, #22c55e 100%); padding: 28px; border-radius: 20px; color: white; margin-bottom: 18px;}
.card {background: white; border-radius: 16px; padding: 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #eef2ee; margin-bottom: 12px;}
.badge {background:#dcfce7; color:#166534; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;}
.badge-red {background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:20px; font-size:12px;}
.inbox-item {border-left:4px solid #22c55e; background:#f8faf8; padding:12px; border-radius:10px; margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

ADMIN_EMAIL = "harphen-prog@gmail.com"
STRIPE_LINK = "https://buy.stripe.com/test_00g5kL2V0"
AFF_FILE = "affiliates.json"
SUB_FILE = "submissions.json"

if os.path.exists(AFF_FILE):
    try:
        with open(AFF_FILE) as f: AFF=json.load(f)
    except: AFF={}
else:
    AFF={"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood","Black-Eyed Susan":"https://amazon.com/s?k=black+eyed+susan","Hydrangea":"https://amazon.com/s?k=hydrangea"}

if os.path.exists(SUB_FILE):
    try:
        with open(SUB_FILE) as f: SUBS=json.load(f)
    except: SUBS=[]
else: SUBS=[]

if "users" not in st.session_state: st.session_state.users={ADMIN_EMAIL: {"pw":"admin123","plan":"paid","role":"admin"}}
if "login" not in st.session_state: st.session_state.login=None
if "unlocked" not in st.session_state: st.session_state.unlocked=False
def is_admin(): return st.session_state.login and st.session_state.users.get(st.session_state.login,{}).get("role")=="admin"
def save_subs():
    with open(SUB_FILE,"w") as f: json.dump(SUBS,f,indent=2)

with st.sidebar:
    st.title("🌿 YardScan Pro")
    if st.session_state.login:
        st.success(f"{st.session_state.login}")
        plan=st.session_state.users[st.session_state.login]["plan"]
        st.markdown(f"<span class='badge'>{plan.upper()} PLAN</span>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.login=None; st.session_state.unlocked=False; st.rerun()
        if is_admin():
            st.divider()
            st.subheader(f"📥 Client Inbox ({len(SUBS)})")
            st.caption("All client jobs land here")
            if st.button("View All Jobs", use_container_width=True): st.session_state.show_inbox=True
            st.divider()
            st.subheader("🔧 Affiliate Links")
            txt=st.text_area("JSON", json.dumps(AFF,indent=2), height=150)
            if st.button("Save Links"):
                with open(AFF_FILE,"w") as f: f.write(txt); st.success("Saved!")
    else:
        t1,t2=st.tabs(["Login","Sign Up"])
        with t1:
            e=st.text_input("Email", key="l1"); p=st.text_input("Password", type="password", key="l2")
            if st.button("Login", type="primary", use_container_width=True):
                if e in st.session_state.users and st.session_state.users[e]["pw"]==p:
                    st.session_state.login=e
                    if st.session_state.users[e]["plan"]=="paid": st.session_state.unlocked=True
                    st.rerun()
                else: st.error(f"Use {ADMIN_EMAIL} / admin123")
        with t2:
            ne=st.text_input("New Email", key="s1"); np=st.text_input("New Pass", type="password", key="s2")
            if st.button("Create Free Account", use_container_width=True):
                st.session_state.users[ne]={"pw":np,"plan":"free","role":"user"}; st.success("Created! Login now.")

if not st.session_state.login:
    st.markdown('<div class="hero"><h1 style="color:white;margin:0;">AI Garden Designer That Sells Plants For You</h1><p>Upload yard → Get removal + design + AI visual + buy links that pay YOU</p></div>', unsafe_allow_html=True)
    st.info("Login from sidebar to start - Free accounts work like client view")
    st.stop()

plan=st.session_state.users[st.session_state.login]["plan"]
paid=(plan=="paid") or st.session_state.unlocked

# ADMIN INBOX VIEW
if is_admin() and st.session_state.get("show_inbox", False):
    st.markdown(f'<div class="hero"><h2 style="color:white;margin:0;">📥 Admin Inbox - {len(SUBS)} Client Jobs</h2><p>Here is where you receive all client files & service requests</p></div>', unsafe_allow_html=True)
    if st.button("← Back to Designer"): st.session_state.show_inbox=False; st.rerun()
    if not SUBS: st.warning("No client jobs yet. Create a test client account and submit.")
    else:
        for idx, job in enumerate(reversed(SUBS)):
            with st.container():
                st.markdown(f'<div class="inbox-item"><b>#{len(SUBS)-idx} {job["client_name"]}</b> • {job["client_email"]} • Zip {job["zip"]} • <b>{job["service"]}</b> • {job["date"]} • {"PAID" if job["paid"] else "FREE"}<br>{job["notes"]}</div>', unsafe_allow_html=True)
                if st.button(f"View Photos Job #{len(SUBS)-idx}", key=f"v{idx}"):
                    st.json(job)
    st.stop()

# NORMAL DESIGNER VIEW
st.markdown(f'<div class="hero"><h2 style="color:white;margin:0;">Welcome back, {st.session_state.login.split("@")[0]}! 🌿</h2><p>Zip-native plants • Pro report • Client-ready</p></div>', unsafe_allow_html=True)

# CLIENT INFO FORM - THIS IS WHAT YOU RECEIVE
st.markdown("### 👤 Client Info & Service Requested (This goes to your Inbox)")
c1,c2,c3=st.columns(3)
with c1: client_name=st.text_input("Client Full Name", placeholder="John Smith")
with c2: client_email=st.text_input("Client Email (for delivery)", value=st.session_state.login)
with c3: service=st.selectbox("Service Needed", ["Full Yard Design $49","Removal Plan Only $29","New Planting Only $29","AI Visual Only $19","On-site Consultation $149"])

notes=st.text_area("What does client want? (e.g. low maintenance, pet friendly, privacy)", placeholder="I want low maintenance, colorful, privacy from neighbors...")
st.divider()

cL,cR=st.columns([3,1])
with cL:
    zipc=st.text_input("📍 Client Zip Code", "19426")
    ups=st.file_uploader("📸 Upload 1-4 Yard Photos", accept_multiple_files=True, type=["jpg","jpeg","png"])
with cR:
    if not paid:
        st.error("🔒 PAID LOCKED")
        st.link_button("Unlock $49 →", STRIPE_LINK, use_container_width=True)
        if st.button("I Paid - Unlock"): st.session_state.unlocked=True; st.rerun()
    else:
        st.success("✅ PAID - Full Unlocked")

if ups and st.button("✨ Generate & Send to Admin Inbox", type="primary", use_container_width=True):
    # SAVE TO INBOX
    job={"client_name":client_name or st.session_state.login.split("@")[0], "client_email":client_email, "zip":zipc, "service":service, "notes":notes, "date":str(datetime.datetime.now())[:19], "paid":paid, "photo_count":len(ups)}
    SUBS.append(job); save_subs()
    st.balloons(); st.success(f"✅ Submitted! Admin will see this in Inbox - Job #{len(SUBS)}")

    st.header(f"Report - Zip {zipc} - {service}")
    col1,col2=st.columns(2)
    with col1:
        st.subheader("1. Removal / Keep Plan")
        if paid:
            st.markdown('<div class="card"><span class="badge-red">REMOVE</span> <b>Juniper front window</b> - Blocks light</div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><span class="badge">KEEP</span> <b>Mature Maple</b> - Great shade</div>', unsafe_allow_html=True)
        else: st.info("🔒 Paid: Full removal plan - 1 preview")
    with col2:
        st.image(ups[0], caption="Original - Client upload")
        if paid: st.image(ups[0], caption="AI Proposed: lavender + boxwood")

    st.subheader("2. New Plants (with YOUR affiliate links)")
    plants=[{"name":"Lavender","why":"Purple, fragrant","price":"$14.99"},{"name":"Boxwood","why":"Evergreen","price":"$29.99"},{"name":"Black-Eyed Susan","why":"Native","price":"$11.99"},{"name":"Hydrangea","why":"Bloom","price":"$34.99"}]
    cols=st.columns(2)
    for i,pl in enumerate(plants):
        with cols[i%2]:
            st.markdown(f'<div class="card"><h4>{pl["name"]}</h4><p>{pl["why"]}</p><b>{pl["price"]}</b></div>', unsafe_allow_html=True)
            if paid: st.link_button(f"Buy {pl['name']}", AFF.get(pl["name"],"#"), use_container_width=True)
