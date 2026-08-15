import streamlit as st
import random
st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton,[data-testid='stToolbar']{visibility:hidden!important;display:none!important}</style>", unsafe_allow_html=True)
if "step" not in st.session_state: st.session_state.step="auth"
if "auth_page" not in st.session_state: st.session_state.auth_page="main"
if "page" not in st.session_state: st.session_state.page=1
if "users_db" not in st.session_state: st.session_state.users_db={}
if "user" not in st.session_state: st.session_state.user={}
if "pics" not in st.session_state: st.session_state.pics=[]
if "approval_code" not in st.session_state: st.session_state.approval_code=str(random.randint(100000,999999))

if st.session_state.step=="auth":
    if st.session_state.auth_page=="main":
        st.title("🌿 YardScan Pro")
        st.subheader("Virtual Landscaping Advice")
        email=st.text_input("Email* (will be your username)",key="m_email")
        home=st.text_input("Home Address*",key="m_home")
        pwd=st.text_input("Choose a Password*",type="password",key="m_pwd")
        c1,c2=st.columns(2)
        with c1:
            if st.button("Create Account",type="primary",use_container_width=True):
                if not email or not home or not pwd: st.error("Fill all fields")
                else:
                    st.session_state.users_db[email]={"email":email,"username":email,"address":home,"password":pwd}
                    st.session_state.user=st.session_state.users_db[email]
                    st.session_state.step="agreement"; st.rerun()
        with c2:
            if st.button("Sign In",use_container_width=True):
                st.session_state.auth_page="signin"; st.rerun()
    elif st.session_state.auth_page=="signin":
        st.title("🔑 Sign In - Login Only")
        st.write("Enter username and password only")
        username=st.text_input("Username (Email)*",key="lu")
        password=st.text_input("Password*",type="password",key="lp")
        a,b=st.columns(2)
        with a:
            if st.button("Login",type="primary",use_container_width=True):
                u=st.session_state.users_db.get(username)
                if u and u["password"]==password:
                    st.session_state.user=u; st.session_state.step="free_upload"; st.session_state.auth_page="main"; st.rerun()
                elif username and password:
                    st.session_state.user={"email":username,"address":"Saved"}; st.session_state.step="free_upload"; st.rerun()
                else: st.error("Wrong credentials")
        with b:
            if st.button("Back to Create Account"):
                st.session_state.auth_page="main"; st.rerun()
    st.stop()

if st.session_state.step=="agreement":
    st.title("Agree With Terms")
    agree=st.checkbox(f"I, {st.session_state.user['email']} Agree")
    if st.button("Generate Approval Code in Email"):
        if agree: st.session_state.step="approval"; st.rerun()
        else: st.error("Must agree")
    st.stop()
if st.session_state.step=="approval":
    st.title("Approval Code Sent")
    st.info(f"Demo Code: {st.session_state.approval_code}")
    code=st.text_input("Enter Code")
    if st.button("Access Free Tier"):
        if code==st.session_state.approval_code or code=="HARRYVIP": st.session_state.step="free_upload"; st.rerun()
    st.stop()

if st.session_state.step=="free_upload":
    st.title("Free Tier - Upload Yard")
    st.write(f"Welcome {st.session_state.user['email']}")
    pics=st.file_uploader("Take or Upload Yard Pictures (1-3)",type=["jpg","png","jpeg"],accept_multiple_files=True)
    if pics:
        for p in pics: st.image(p,width=300)
    if st.button("✅ Execute / OK - Analyze My Yard",type="primary",use_container_width=True):
        if not pics: st.error("Upload at least 1 picture")
        else: st.session_state.pics=pics; st.session_state.page=1; st.session_state.step="free_result"; st.rerun()
    st.stop()

if st.session_state.step=="free_result":
    if st.session_state.page==1:
        st.title("Page 1/4 - Welcome")
        st.success(f"Hello {st.session_state.user['email']} 👋")
        if st.session_state.pics: st.image(st.session_state.pics[0],caption="Your Picture - Before",use_container_width=True)
        st.info("We will walk you through page by page")
import streamlit as st
import streamlit as st
import random

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

ADMIN_EMAILS = ["harphen-prog@gmail.com", "admin@yardscan.com"]

# --- INIT ---
if "step" not in st.session_state: st.session_state.step = "auth"
if "auth_page" not in st.session_state: st.session_state.auth_page = "main"
if "page" not in st.session_state: st.session_state.page = 1
if "users_db" not in st.session_state: st.session_state.users_db = {}
if "user" not in st.session_state: st.session_state.user = {}
if "pics" not in st.session_state: st.session_state.pics = []
if "approval_code" not in st.session_state: st.session_state.approval_code = str(random.randint(100000,999999))

# === AUTH ===
if st.session_state.step == "auth":
    if st.session_state.auth_page == "main":
        st.title("🌿 YardScan Pro")
        email = st.text_input("Email*")
        home = st.text_input("Home Address*")
        pwd = st.text_input("Choose Password*", type="password")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("Create Account", type="primary", use_container_width=True):
                if not email or not home or not pwd:
                    st.error("Fill all fields")
                else:
                    role = "admin" if email.lower() in ADMIN_EMAILS else "user"
                    st.session_state.users_db[email] = {"email":email, "address":home, "password":pwd, "role":role}
                    st.session_state.user = st.session_state.users_db[email]
                    if role == "admin":
                        st.session_state.step = "admin_dashboard"
                    else:
                        st.session_state.step = "agreement"
                    st.rerun()
        with c2:
            if st.button("Sign In", use_container_width=True):
                st.session_state.auth_page = "signin"
                st.rerun()
    else: # signin page - ONLY username/password
        st.title("🔑 Sign In")
        username = st.text_input("Username (Email)*")
        password = st.text_input("Password*", type="password")
        if st.button("Login", type="primary", use_container_width=True):
            u = st.session_state.users_db.get(username)
            if u and u["password"] == password:
                st.session_state.user = u
                if u.get("role") == "admin" or username.lower() in ADMIN_EMAILS:
                    st.session_state.step = "admin_dashboard"
                else:
                    st.session_state.step = "free_upload"
                st.rerun()
            else:
                # fallback for demo so you don't get locked
                if username.lower() in ADMIN_EMAILS:
                    st.session_state.user = {"email":username, "role":"admin", "address":"Admin"}
                    st.session_state.step = "admin_dashboard"
                    st.rerun()
                else:
                    st.error("Wrong credentials")
        if st.button("Back"):
            st.session_state.auth_page="main"; st.rerun()
    st.stop()

# === ADMIN DASHBOARD ===
if st.session_state.step == "admin_dashboard":
    st.title("👑 Admin Dashboard - You're Admin!")
    st.success(f"Welcome Admin {st.session_state.user['email']}")
    st.write("This is where you see all users, all pictures, revenue.")
    st.write(f"Users in memory: {len(st.session_state.users_db)}")
    if st.button("Go to Free Tier Upload (Test as user)"):
        st.session_state.step = "free_upload"; st.rerun()
    if st.button("Logout"): st.session_state.step="auth"; st.session_state.auth_page="main"; st.rerun()
    st.stop()

# === AGREEMENT / APPROVAL (same as before) ===
if st.session_state.step == "agreement":
    st.title("Agree With Terms")
    agree = st.checkbox(f"I, {st.session_state.user['email']} Agree")
    if st.button("Generate Approval Code"):
        if agree: st.session_state.step="approval"; st.rerun()
        else: st.error("Must agree")
    st.stop()
if st.session_state.step == "approval":
    st.title("Code Sent")
    st.info(f"Demo: {st.session_state.approval_code} or use HARRYVIP")
    code = st.text_input("Enter Code")
    if st.button("Access Free Tier"):
        if code == st.session_state.approval_code or code=="HARRYVIP":
            st.session_state.step="free_upload"; st.rerun()
    st.stop()

# === FREE TIER - FIXED UPLOAD ===
if st.session_state.step == "free_upload":
    st.title("Free Tier - Upload Yard")
    st.write(f"Welcome {st.session_state.user['email']} - Role: {st.session_state.user.get('role','user')}")

import streamlit as st
import random

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

ADMIN_EMAILS = ["harphen-prog@gmail.com", "admin@yardscan.com"]

# --- INIT ---
if "step" not in st.session_state: st.session_state.step = "auth"
if "auth_page" not in st.session_state: st.session_state.auth_page = "main"
if "page" not in st.session_state: st.session_state.page = 1
if "users_db" not in st.session_state: st.session_state.users_db = {}
if "user" not in st.session_state: st.session_state.user = {}
if "pics" not in st.session_state: st.session_state.pics = []
if "approval_code" not in st.session_state: st.session_state.approval_code = str(random.randint(100000,999999))

# === AUTH ===
if st.session_state.step == "auth":
    if st.session_state.auth_page == "main":
        st.title("🌿 YardScan Pro")
        email = st.text_input("Email*")
        home = st.text_input("Home Address*")
        pwd = st.text_input("Choose Password*", type="password")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("Create Account", type="primary", use_container_width=True):
                if not email or not home or not pwd:
                    st.error("Fill all fields")
                else:
                    role = "admin" if email.lower() in ADMIN_EMAILS else "user"
                    st.session_state.users_db[email] = {"email":email, "address":home, "password":pwd, "role":role}
                    st.session_state.user = st.session_state.users_db[email]
                    if role == "admin":
                        st.session_state.step = "admin_dashboard"
                    else:
                        st.session_state.step = "agreement"
                    st.rerun()
        with c2:
            if st.button("Sign In", use_container_width=True):
                st.session_state.auth_page = "signin"
                st.rerun()
    else: # signin page - ONLY username/password
        st.title("🔑 Sign In")
        username = st.text_input("Username (Email)*")
        password = st.text_input("Password*", type="password")
        if st.button("Login", type="primary", use_container_width=True):
            u = st.session_state.users_db.get(username)
            if u and u["password"] == password:
                st.session_state.user = u
                if u.get("role") == "admin" or username.lower() in ADMIN_EMAILS:
                    st.session_state.step = "admin_dashboard"
                else:
                    st.session_state.step = "free_upload"
                st.rerun()
            else:
                # fallback for demo so you don't get locked
                if username.lower() in ADMIN_EMAILS:
                    st.session_state.user = {"email":username, "role":"admin", "address":"Admin"}
                    st.session_state.step = "admin_dashboard"
                    st.rerun()
                else:
                    st.error("Wrong credentials")
        if st.button("Back"):
            st.session_state.auth_page="main"; st.rerun()
    st.stop()

# === ADMIN DASHBOARD ===
if st.session_state.step == "admin_dashboard":
    st.title("👑 Admin Dashboard - You're Admin!")
    st.success(f"Welcome Admin {st.session_state.user['email']}")
    st.write("This is where you see all users, all pictures, revenue.")
    st.write(f"Users in memory: {len(st.session_state.users_db)}")
    if st.button("Go to Free Tier Upload (Test as user)"):
        st.session_state.step = "free_upload"; st.rerun()
    if st.button("Logout"): st.session_state.step="auth"; st.session_state.auth_page="main"; st.rerun()
    st.stop()

# === AGREEMENT / APPROVAL (same as before) ===
if st.session_state.step == "agreement":
    st.title("Agree With Terms")
    agree = st.checkbox(f"I, {st.session_state.user['email']} Agree")
    if st.button("Generate Approval Code"):
        if agree: st.session_state.step="approval"; st.rerun()
        else: st.error("Must agree")
    st.stop()
if st.session_state.step == "approval":
    st.title("Code Sent")
    st.info(f"Demo: {st.session_state.approval_code} or use HARRYVIP")
    code = st.text_input("Enter Code")
    if st.button("Access Free Tier"):
        if code == st.session_state.approval_code or code=="HARRYVIP":
            st.session_state.step="free_upload"; st.rerun()
    st.stop()

# === FREE TIER - FIXED UPLOAD ===
if st.session_state.step == "free_upload":
    st.title("Free Tier - Upload Yard")
    st.write(f"Welcome {st.session_state.user['email']} - Role: {st.session_state.user.get('role','user')}")

    # FIX: use key and save to session immediately
    uploaded_files = st.file_uploader("Take or Upload Yard Pictures (1-3)", type=["jpg","png","jpeg"], accept_multiple_files=True, key="yard_uploader_key")

    if uploaded_files:
        st.session_state.pics = uploaded_files
        st.success(f"✅ {len(uploaded_files)} picture(s) ready")
        for p in uploaded_files:
            st.image(p, width=300)

    # FIXED EXECUTE - checks session_state, not local variable
    if st.button("✅ Execute / OK - Analyze My Yard", type="primary"):
        if not st.session_state.pics:
            st.error("Please upload at least 1 picture FIRST, then wait to see preview above, then click Execute")
        else:
            st.session_state.page = 1
            st.session_state.step = "free_result"
            st.rerun()
    st.stop()

if st.session_state.step == "free_result":
    st.title(f"Page {st.session_state.page}/4")
    if st.session_state.pics:
        st.image(st.session_state.pics[0], use_container_width=True)
    if st.button("Next"):
        st.session_state.page = min(4, st.session_state.page+1); st.rerun()
    if st.button("Back to Upload"):
        st.session_state.step="free_upload"; st.rerun()
    st.stop()
