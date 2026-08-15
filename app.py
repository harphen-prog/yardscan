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
        if st.button("Next → Plant Identification"): st.session_state.page=2; st.rerun()
    elif st.session_state.page==2:
        st.title("Page 2/4 - Plant Identification")
        if st.session_state.pics: st.image(st.session_state.pics[0],width=350)
        st.markdown("- Boxwood overcrowded, Weeds, Compacted soil, Hosta spots\n- Sun: Full Sun South")
        if st.button("Next → Suggestions"): st.session_state.page=3; st.rerun()
    elif st.session_state.page==3:
        st.title("Page 3/4 - Suggestions & Advice")
        st.write("Thin boxwood 30%, add compost, 3in mulch. Replace 2 with Allium Millenium. Add Zinnia, Hydrangea")
        if st.button("Next → Before / After"): st.session_state.page=4; st.rerun()
    elif st.session_state.page==4:
        st.title("Page 4/4 - Your New Look")
        c1,c2=st.columns(2)
        with c1:
            st.subheader("Before")
            if st.session_state.pics: st.image(st.session_state.pics[0],use_container_width=True)
        with c2:
            st.subheader("After - Suggested")
            st.image("https://images.unsplash.com/photo-1558618666-fcd25c85cd64",caption="With Allium + Zinnia beds",use_container_width=True)
        if st.button("Start Over"): st.session_state.step="free_upload"; st.rerun()
    st.stop()    pwd = st.text_input("Choose a Password*", type="password")

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
