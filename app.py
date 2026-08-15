import streamlit as st
import random
st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")
ADMIN_EMAILS = ["harphen-prog@gmail.com"]

if "step" not in st.session_state: st.session_state.step="auth"
if "auth_page" not in st.session_state: st.session_state.auth_page="main"
if "pics" not in st.session_state: st.session_state.pics=[]
if "users_db" not in st.session_state: st.session_state.users_db={"harphen-prog@gmail.com":{"email":"harphen-prog@gmail.com","address":"Admin","password":"admin","role":"admin"}}
if "user" not in st.session_state: st.session_state.user={}
if "approval_code" not in st.session_state: st.session_state.approval_code=str(random.randint(100000,999999))
if "page" not in st.session_state: st.session_state.page=1

# AUTH
if st.session_state.step=="auth":
    if st.session_state.auth_page=="main":
        st.title("🌿 YardScan Pro")
        email=st.text_input("Email*"); home=st.text_input("Home Address*"); pwd=st.text_input("Password*",type="password")
        c1,c2=st.columns(2)
        with c1:
            if st.button("Create Account",type="primary",use_container_width=True):
                role="admin" if email.lower() in ADMIN_EMAILS else "user"
                st.session_state.users_db[email]={"email":email,"address":home,"password":pwd,"role":role}
                st.session_state.user=st.session_state.users_db[email]
                st.session_state.step="admin_dashboard" if role=="admin" else "agreement"; st.rerun()
        with c2:
            if st.button("Sign In",use_container_width=True):
                st.session_state.auth_page="signin"; st.rerun()
    else:
        st.title("🔑 Sign In"); username=st.text_input("Username (Email)*"); password=st.text_input("Password*",type="password")
        if st.button("Login",type="primary",use_container_width=True):
            if username.lower() in ADMIN_EMAILS:
                st.session_state.user={"email":username,"role":"admin","address":"Admin"}; st.session_state.step="admin_dashboard"; st.rerun()
            u=st.session_state.users_db.get(username)
            if u and u["password"]==password:
                st.session_state.user=u; st.session_state.step="admin_dashboard" if u.get("role")=="admin" else "free_upload"; st.rerun()
            else: st.error("Wrong credentials")
        if st.button("Back"): st.session_state.auth_page="main"; st.rerun()
    st.stop()

# ADMIN DASHBOARD - FULL ACCESS
if st.session_state.step=="admin_dashboard":
    st.title("👑 Admin Dashboard - Full Access")
    st.success(f"Admin: {st.session_state.user['email']}")
    tab1, tab2, tab3 = st.tabs(["🌿 Yard Analyzer (All Access)", "👥 Users", "⚙️ System"])

    with tab1:
        st.subheader("Upload & Analyze Yard - Admin has full pro access")
        with st.form("admin_upload"):
            uploaded = st.file_uploader("Upload Yard Pictures (1-3)", type=["jpg","jpeg","png"], accept_multiple_files=True)
            cam = st.camera_input("Or Take Photo")
            submit = st.form_submit_button("📤 Upload", type="primary")
            if submit:
                pics=[]
                if uploaded: pics.extend(uploaded)
                if cam: pics.append(cam)
                if pics:
                    st.session_state.pics=pics; st.success(f"✅ {len(pics)} saved")
                else: st.error("Select at least 1")

        if st.session_state.pics:
            st.divider()
            for p in st.session_state.pics: st.image(p, width=300)
            if st.button("✅ Execute / Analyze My Yard", type="primary"):
                st.session_state.page=1; st.session_state.step="result"; st.rerun()

    with tab2:
        st.subheader(f"Total Users: {len(st.session_state.users_db)}")
        for email, data in st.session_state.users_db.items():
            st.write(f"- {email} | Role: {data.get('role','user')} | Addr: {data.get('address','')}")

    with tab3:
        st.write("System Status: Steady")
        st.write("Storage: Using memory now - for 100+ users add Supabase Storage")
        st.write("Speed: Add @st.cache_data for plant analysis to stay fast")
        if st.button("Logout"): st.session_state.step="auth"; st.rerun()
    st.stop()

# FREE TIER USER FLOW (non-admin)
if st.session_state.step=="agreement":
    st.title("Agree"); agree=st.checkbox(f"I {st.session_state.user['email']} Agree")
    if st.button("Generate Code"):
        if agree: st.session_state.step="approval"; st.rerun()
        else: st.error("Must agree")
    st.stop()
if st.session_state.step=="approval":
    st.title("Code"); st.info(f"Demo: {st.session_state.approval_code} or HARRYVIP")
    code=st.text_input("Enter Code")
    if st.button("Access Free Tier"):
        if code==st.session_state.approval_code or code=="HARRYVIP": st.session_state.step="free_upload"; st.rerun()
    st.stop()
if st.session_state.step=="free_upload":
    st.title("Free Tier - Upload Yard"); st.write(f"Welcome {st.session_state.user['email']}")
    with st.form("free_form"):
        up=st.file_uploader("Upload (1-3)", type=["jpg","jpeg","png"], accept_multiple_files=True)
        cam=st.camera_input("Camera")
        sub=st.form_submit_button("📤 Upload", type="primary")
        if sub:
            pics=[]
            if up: pics.extend(up)
            if cam: pics.append(cam)
            if pics: st.session_state.pics=pics; st.success("Saved")
            else: st.error("Select picture")
    if st.session_state.pics:
        for p in st.session_state.pics: st.image(p,width=300)
        if st.button("✅ Execute / OK - Analyze",type="primary"): st.session_state.page=1; st.session_state.step="result"; st.rerun()
    st.stop()

if st.session_state.step=="result":
    st.title(f"Page {st.session_state.page}/4 - Results")
    if st.session_state.pics: st.image(st.session_state.pics[0],use_container_width=True)
    if st.session_state.page==1: st.info("Welcome - Boxwood overcrowded")
    if st.session_state.page==2: st.info("Plant ID: Boxwood, Hosta, Weeds")
    if st.session_state.page==3: st.info("Suggestions: Thin 30%, add mulch, Allium")
    if st.session_state.page==4:
        st.success("Before/After Ready")
        st.image("https://images.unsplash.com/photo-1558618666-fcd25c85cd64",caption="After",use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        if st.session_state.page<4 and st.button("Next →"): st.session_state.page+=1; st.rerun()
    with c2:
        if st.button("Back to Dashboard"):
            if st.session_state.user.get("role")=="admin" or st.session_state.user["email"].lower() in ADMIN_EMAILS:
                st.session_state.step="admin_dashboard"
            else: st.session_state.step="free_upload"
            st.rerun()
    st.stop()
