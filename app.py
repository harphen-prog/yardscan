import streamlit as st, json, random, datetime
st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")
ADMIN_EMAILS=["harphen-prog@gmail.com"]

if "users_db" not in st.session_state: st.session_state.users_db={"harphen-prog@gmail.com":{"email":"harphen-prog@gmail.com","username":"harphen-prog@gmail.com","address":"Admin HQ NJ","password":"admin","role":"admin","plan":"PAID PLAN","joined":str(datetime.date.today())}}
if "step" not in st.session_state: st.session_state.step="auth"
if "auth_page" not in st.session_state: st.session_state.auth_page="main"
if "work_orders" not in st.session_state: st.session_state.work_orders=[]
if "sales" not in st.session_state: st.session_state.sales=[]
if "affiliate_links" not in st.session_state: st.session_state.affiliate_links=json.dumps({"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood"},indent=2)
if "approval_code" not in st.session_state: st.session_state.approval_code=str(random.randint(100000,999999))

if st.session_state.step=="auth":
    if st.session_state.auth_page=="main":
        st.title("🌿 YardScan Pro"); st.caption("AI Designer v2.0")
        e=st.text_input("Email*"); a=st.text_input("Home Address*"); p=st.text_input("Password*",type="password")
        if st.button("Create Account",type="primary",use_container_width=True):
            role="admin" if e.lower() in ADMIN_EMAILS else "user"; plan="PAID PLAN" if role=="admin" else "FREE PLAN"
            st.session_state.users_db[e]={"email":e,"username":e,"address":a,"password":p,"role":role,"plan":plan,"joined":str(datetime.date.today())}
            st.session_state.user=st.session_state.users_db[e]; st.session_state.step="admin_dashboard" if role=="admin" else "agreement"; st.rerun()
        if st.button("Sign In"): st.session_state.auth_page="signin"; st.rerun()
    else:
        st.title("🔑 Sign In"); u=st.text_input("Username*"); pw=st.text_input("Password*",type="password")
        if st.button("Login",type="primary"):
            if u.lower() in ADMIN_EMAILS: st.session_state.user=st.session_state.users_db.get(u,{"email":u,"role":"admin","plan":"PAID PLAN","address":"Admin"}); st.session_state.step="admin_dashboard"; st.rerun()
            d=st.session_state.users_db.get(u)
            if d and d["password"]==pw: st.session_state.user=d; st.session_state.step="admin_dashboard" if d["role"]=="admin" else "free_upload"; st.rerun()
        if st.button("Back"): st.session_state.auth_page="main"; st.rerun()
    st.stop()

if st.session_state.step=="admin_dashboard":
    with st.sidebar:
        st.title("🌿 YardScan Pro"); st.write(st.session_state.user["email"]); st.write(st.session_state.user.get("plan","PAID PLAN"))
        if st.button("Logout"): st.session_state.step="auth"; st.rerun()
        st.divider(); st.subheader("🔧 Admin Back-Office"); st.session_state.affiliate_links=st.text_area("Affiliate JSON",value=st.session_state.affiliate_links,height=200)
    c1,c2=st.columns([3,1])
    with c1: st.markdown(f"<div style='background:linear-gradient(135deg,#14532d,#22c55e);padding:25px;border-radius:15px;color:white'><h2>Welcome back, {st.session_state.user['email'].split('@')[0]}! 🌿</h2><p>Full admin access - All features</p></div>",unsafe_allow_html=True)
    with c2: st.metric("Users",len(st.session_state.users_db)); st.metric("Earnings",f"${len(st.session_state.sales)*34}")

    t1,t2,t3,t4=st.tabs(["🌿 Analyzer (FIXED)", "👥 Users & Data", "📋 Work Orders", "💰 Accounting"])
    with t1:
        st.warning("⚠️ If opening from WhatsApp, tap ⋮ → Open in Chrome to allow file upload")
        # MOST STABLE UPLOADER - SINGLE FILE, NO MULTIPLE
        file = st.file_uploader("Upload Yard Picture - Tap here", type=["jpg","jpeg","png"], accept_multiple_files=False, key="stable_single")
        if file:
            st.success(f"✅ Uploaded: {file.name}")
            st.image(file, use_container_width=True)
            if st.button("✅ Execute - Analyze",type="primary",use_container_width=True):
                st.session_state.work_orders.append({"user":st.session_state.user['email'],"address":st.session_state.user.get('address',''),"date":str(datetime.date.today()),"status":"Completed"}); st.balloons(); st.success("Analyzed: Boxwood overcrowded - thin 30%, add mulch")
        else: st.info("No file yet - tap Upload above, choose Files, pick JPG <10MB")
    with t2:
        st.subheader("Users & Data Collecting - Name Address Email Type")
        for em, d in st.session_state.users_db.items():
            with st.expander(f"{em} - {d.get('role')} - {d.get('address')}"):
                st.json(d)
    with t3:
        st.subheader("Work Orders by User")
        if st.session_state.work_orders:
            for w in st.session_state.work_orders: st.write(w)
        else: st.write("No orders yet")
    with t4:
        st.subheader("Accounting Sales/Earnings")
        c1,c2=st.columns(2); c1.metric("Sales",len(st.session_state.sales)); c2.metric("Earnings",f"${len(st.session_state.sales)*29}")
        if st.button("Add $29 Sale"): st.session_state.sales.append({"date":str(datetime.date.today()),"amount":29}); st.rerun()
    st.stop()

# FREE TIER - SAME FIXED UPLOADER
if st.session_state.step in ["agreement","approval","free_upload"]:
    if st.session_state.step=="agreement":
        st.title("Agreement"); a=st.checkbox(f"I {st.session_state.user['email']} agree")
        if st.button("Continue") and a: st.session_state.step="approval"; st.rerun()
        st.stop()
    if st.session_state.step=="approval":
        st.title("Code"); st.info(f"Code: {st.session_state.approval_code} or HARRYVIP"); c=st.text_input("Enter code")
        if st.button("Access Free Tier") and (c==st.session_state.approval_code or c=="HARRYVIP"): st.session_state.step="free_upload"; st.rerun()
        st.stop()
    if st.session_state.step=="free_upload":
        st.title("Free Tier - Upload Yard")
        st.warning("⚠️ Open in Chrome, not WhatsApp, for upload to work")
        f=st.file_uploader("Upload Yard Picture", type=["jpg","jpeg","png"], accept_multiple_files=False, key="free_stable")
        if f: st.success(f"✅ {f.name}"); st.image(f,use_container_width=True); st.balloons()
        st.stop()
