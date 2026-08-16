import streamlit as st
import random, json, datetime

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")
ADMIN_EMAILS = ["harphen-prog@gmail.com"]

# INIT
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "harphen-prog@gmail.com": {"email":"harphen-prog@gmail.com","username":"harphen-prog@gmail.com","address":"Admin HQ - Lawrenceville, NJ","password":"admin","role":"admin","plan":"PAID PLAN","joined":"2025-01-01","phone":""}
    }
if "step" not in st.session_state: st.session_state.step="auth"
if "auth_page" not in st.session_state: st.session_state.auth_page="main"
if "pics" not in st.session_state: st.session_state.pics=[]
if "work_orders" not in st.session_state: st.session_state.work_orders=[]
if "sales" not in st.session_state: st.session_state.sales=[]
if "affiliate_links" not in st.session_state:
    st.session_state.affiliate_links = json.dumps({
        "Lavender": "https://amazon.com/s?k=lavender+plant",
        "Boxwood": "https://amazon.com/s?k=boxwood+shrub",
        "Black-Eyed Susan": "https://amazon.com/s?k=black+eyed+susan",
        "Hydrangea": "https://amazon.com/s?k=hydrangea"
    }, indent=2)
if "approval_code" not in st.session_state: st.session_state.approval_code=str(random.randint(100000,999999))

# AUTH
if st.session_state.step=="auth":
    if st.session_state.auth_page=="main":
        st.title("🌿 YardScan Pro")
        st.caption("AI Landscape Designer v2.0")
        email=st.text_input("Email* (becomes username)"); addr=st.text_input("Home Address*"); pwd=st.text_input("Password*",type="password")
        c1,c2=st.columns(2)
        with c1:
            if st.button("Create Account",type="primary",use_container_width=True):
                if not email or not addr or not pwd: st.error("Fill all")
                else:
                    role="admin" if email.lower() in ADMIN_EMAILS else "user"
                    plan="PAID PLAN" if role=="admin" else "FREE PLAN"
                    st.session_state.users_db[email]={"email":email,"username":email,"address":addr,"password":pwd,"role":role,"plan":plan,"joined":str(datetime.date.today()),"phone":""}
                    st.session_state.user=st.session_state.users_db[email]
                    st.session_state.step="admin_dashboard" if role=="admin" else "agreement"; st.rerun()
        with c2:
            if st.button("Sign In",use_container_width=True): st.session_state.auth_page="signin"; st.rerun()
    else:
        st.title("🔑 Sign In"); u=st.text_input("Username (Email)*"); p=st.text_input("Password*",type="password")
        if st.button("Login",type="primary",use_container_width=True):
            if u.lower() in ADMIN_EMAILS:
                if u not in st.session_state.users_db: st.session_state.users_db[u]={"email":u,"username":u,"address":"Admin HQ","password":"admin","role":"admin","plan":"PAID PLAN","joined":str(datetime.date.today()),"phone":""}
                st.session_state.user=st.session_state.users_db[u]; st.session_state.step="admin_dashboard"; st.rerun()
            db=st.session_state.users_db.get(u)
            if db and db["password"]==p:
                st.session_state.user=db; st.session_state.step="admin_dashboard" if db["role"]=="admin" else "free_upload"; st.rerun()
            else: st.error("Wrong username/password")
        if st.button("Back"): st.session_state.auth_page="main"; st.rerun()
    st.stop()

# ===== ADMIN BACK-OFFICE - ORIGINAL DESIGN + FIXED UPLOAD =====
if st.session_state.step=="admin_dashboard":
    # SIDEBAR - like your first version
    with st.sidebar:
        st.title("🌿 YardScan Pro")
        st.caption("AI Landscape Designer v2.0")
        st.markdown(f"**Welcome:** {st.session_state.user['email']}")
        st.markdown(f"**{st.session_state.user.get('plan','PAID PLAN')}**")
        if st.button("Logout"): st.session_state.step="auth"; st.session_state.auth_page="main"; st.rerun()
        st.divider()
        st.subheader("🔧 Admin Back-Office")
        st.caption("Your affiliate links = Your commission")
        st.session_state.affiliate_links=st.text_area("Affiliate Links JSON (editable)", value=st.session_state.affiliate_links, height=250)
        if st.button("💾 Save Links",type="primary",use_container_width=True):
            try: json.loads(st.session_state.affiliate_links); st.success("Saved")
            except: st.error("Invalid JSON")

    # TOP BANNER - fixed bug [3][1] -> [3,1]
    c1,c2=st.columns([3,1])
    with c1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#14532d,#22c55e);padding:28px;border-radius:18px;color:white">
        <h1 style="margin:0">Welcome back, {st.session_state.user['email'].split('@')[0]}! 🌿</h1>
        <p style="margin:6px 0 0 0">Zip-based native plants • Professional report • Client-ready • Full admin access</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.metric("Total Users", len(st.session_state.users_db))
        st.metric("Total Earnings", f"${len(st.session_state.sales)*29 + len(st.session_state.sales)*5}")

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(["🌿 Analyzer", "👥 Users & Data Collecting", "📋 Work Orders", "💰 Accounting"])

    # TAB 1 - FIXED SIMPLE UPLOAD - NO EXTRA CAMERA WIDGET
    with tab1:
        st.subheader("Upload & Analyze Yard - Admin has full pro access")
        st.caption("Tap Upload → Android will ask Camera or Files → Choose Files for gallery")

        # SIMPLE UPLOAD ONLY - Android handles Camera/Files choice itself
        uploaded_files = st.file_uploader("Upload Yard Pictures (1-3)", type=["jpg","jpeg","png"], accept_multiple_files=True, key="yard_upload_final")

        if uploaded_files:
            st.session_state.pics = uploaded_files
            st.success(f"✅ {len(uploaded_files)} picture(s) loaded from file")
            cols=st.columns(3)
            for i, pic in enumerate(uploaded_files[:3]):
                with cols[i % 3]:
                    st.image(pic, caption=f"Yard {i+1}", use_container_width=True)

            if st.button("✅ Execute / OK - Analyze My Yard", type="primary", use_container_width=True):
                st.session_state.work_orders.append({
                    "user": st.session_state.user['email'],
                    "address": st.session_state.user.get('address',''),
                    "date": str(datetime.date.today()),
                    "pics": len(uploaded_files),
                    "status": "Completed",
                    "type": "Analysis"
                })
                st.session_state.step="result"; st.rerun()
        else:
            st.info("👆 Select files above. Preview will appear here after selection.")

    # TAB 2 - USERS & DATA COLLECTING
    with tab2:
        st.subheader("Users List - Type, Name, Address, Email - Data Collecting")
        for email, data in st.session_state.users_db.items():
            with st.expander(f"{email} | {data.get('role','user')} | {data.get('plan','FREE')} | {data.get('address','')}"):
                st.write(f"**Email:** {data['email']}")
                st.write(f"**Username:** {data.get('username',email)}")
                st.write(f"**Address:** {data.get('address','')}")
                st.write(f"**User Type:** {data.get('role','user')}")
                st.write(f"**Plan:** {data.get('plan','FREE')}")
                st.write(f"**Joined:** {data.get('joined','')}")
                # Work orders for this user
                user_orders=[o for o in st.session_state.work_orders if o['user']==email]
                st.write(f"**Work Orders:** {len(user_orders)}")

    # TAB 3 - WORK ORDERS BY USER
    with tab3:
        st.subheader("Work Orders by User")
        if not st.session_state.work_orders: st.info("No work orders yet - upload a yard in Analyzer tab")
        else:
            for wo in st.session_state.work_orders:
                st.markdown(f"**{wo['date']}** - {wo['user']} | {wo['address']} | {wo['pics']} pics | {wo['status']}")

    # TAB 4 - ACCOUNTING
    with tab4:
        st.subheader("Accounting - Sales & Earnings")
        c1,c2,c3=st.columns(3)
        c1.metric("Sales Count", len(st.session_state.sales))
        c2.metric("Sales Earnings", f"${len(st.session_state.sales)*29}")
        c3.metric("Affiliate Earnings", f"${len(st.session_state.sales)*5}")
        st.divider()
        st.write("Data Collecting for Scaling:")
        st.code("For 100+ users: Need Supabase DB for users + Storage for yard pics + sales table. Keeps app fast & steady.")
        if st.button("Simulate $29 Sale"): st.session_state.sales.append({"email":"customer@test.com","amount":29,"date":str(datetime.date.today())}); st.rerun()
        if st.session_state.sales: st.dataframe(st.session_state.sales, use_container_width=True)
    st.stop()

# FREE USER FLOW
if st.session_state.step=="agreement":
    st.title("Agreement"); agree=st.checkbox(f"I {st.session_state.user['email']} Agree")
    if st.button("Continue") and agree: st.session_state.step="approval"; st.rerun()
    st.stop()
if st.session_state.step=="approval":
    st.title("Approval Code"); st.info(f"Code: {st.session_state.approval_code} or HARRYVIP"); code=st.text_input("Enter Code")
    if st.button("Access Free Tier") and (code==st.session_state.approval_code or code=="HARRYVIP"): st.session_state.step="free_upload"; st.rerun()
    st.stop()
if st.session_state.step=="free_upload":
    st.title("Free Tier - Upload Yard")
    up=st.file_uploader("Upload Yard Pictures (1-3)", type=["jpg","jpeg","png"], accept_multiple_files=True, key="free_final")
    if up:
        st.session_state.pics=up
        for p in up: st.image(p, width=300)
        if st.button("✅ Execute", type="primary"): st.session_state.step="result"; st.rerun()
    st.stop()
if st.session_state.step=="result":
    st.title("Results - Before / After")
    if st.session_state.pics: st.image(st.session_state.pics[0], caption="Before - Your Yard", use_container_width=True)
    st.success("Analysis: Boxwood overcrowded, thin 30%, add native Allium, mulch")
    st.image("https://images.unsplash.com/photo-1558618666-fcd25c85cd64", caption="After - Suggestion", use_container_width=True)
    if st.button("Back to Dashboard"): st.session_state.step="admin_dashboard" if st.session_state.user.get("role")=="admin" else "free_upload"; st.rerun()
    st.stop()
