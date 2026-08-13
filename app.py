import streamlit as st, json, os, datetime

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* {font-family: 'Inter', sans-serif;}
.hero {background: linear-gradient(135deg, #0f5c36 0%, #22c55e 100%); padding: 22px; border-radius: 18px; color: white; margin-bottom: 14px;}
.card {background: white; border-radius: 14px; padding: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 8px;}
.price-box {background:#f0fdf4; border:2px solid #22c55e; padding:16px; border-radius:12px; text-align:center;}
</style>
""", unsafe_allow_html=True)

AFF_FILE = "affiliates.json"
SUB_FILE = "submissions.json"
USER_FILE = "users_db.json"

def load_json(f, default):
    if os.path.exists(f):
        try:
            with open(f) as j:
                data=json.load(j)
                if data: return data
        except: pass
    return default

def save_json(f, data):
    with open(f,"w") as j: json.dump(data,j,indent=2)

# PERSISTENT LOAD - Never overwrite if file exists!
AFF = load_json(AFF_FILE, {"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood","Black-Eyed Susan":"https://amazon.com/s?k=black+eyed+susan","Hydrangea":"https://amazon.com/s?k=hydrangea"})
SUBS = load_json(SUB_FILE, [])
DEFAULT_USERS = {"harphen-prog@gmail.com":{"pw":"admin123","name":"Harphen Admin","plan":"paid","role":"admin","address":"","newsletter":False,"purchases":[],"joined":"2026-01-01"}}
USERS = load_json(USER_FILE, DEFAULT_USERS)
# Ensure admin always exists
USERS["harphen-prog@gmail.com"]=DEFAULT_USERS["harphen-prog@gmail.com"]

if "login" not in st.session_state: st.session_state.login=None
if "unlocked" not in st.session_state: st.session_state.unlocked=False
if "show_dashboard" not in st.session_state: st.session_state.show_dashboard=False
if "selected_amount" not in st.session_state: st.session_state.selected_amount=49

def is_admin(): return st.session_state.login and USERS.get(st.session_state.login,{}).get("role")=="admin"
def save_all(): save_json(SUB_FILE, SUBS); save_json(USER_FILE, USERS)

# SIDEBAR
with st.sidebar:
    st.title("🌿 YardScan Pro")
    if st.session_state.login:
        u = USERS.get(st.session_state.login, {})
        st.success(f"{u.get('name','')} \n{st.session_state.login}")
        plan_lbl = f"{u.get('plan','free').upper()} PLAN"
        st.caption(plan_lbl)
        if st.button("Logout", use_container_width=True):
            st.session_state.login=None; st.session_state.unlocked=False; st.session_state.show_dashboard=False; st.rerun()
        if is_admin():
            st.divider()
            st.subheader(f"📊 Admin")
            st.metric("Clients", len([k for k,v in USERS.items() if v.get("role")!="admin"]))
            st.metric("Jobs", len(SUBS))
            st.metric("Newsletter", sum(1 for x in USERS.values() if x.get("newsletter")))
            if st.button("📥 Open Dashboard", type="primary", use_container_width=True):
                st.session_state.show_dashboard=True; st.rerun()
            if st.button("🧑‍🌾 Designer", use_container_width=True):
                st.session_state.show_dashboard=False; st.rerun()
            # BACKUP BUTTON - SO YOU NEVER LOSE CLIENTS
            if st.button("💾 Export Clients CSV"):
                import pandas as pd
                df=pd.DataFrame([{"Name":v.get("name"),"Email":k,"Address":v.get("address"),"Plan":v.get("plan"),"Newsletter":v.get("newsletter")} for k,v in USERS.items() if v.get("role")!="admin"])
                st.download_button("Download CSV", df.to_csv(index=False), "clients_backup.csv", "text/csv")
    else:
        t1,t2=st.tabs(["Login","Sign Up"])
        with t1:
            e=st.text_input("Email*", key="l1"); p=st.text_input("Password*", type="password", key="l2")
            if st.button("Login", type="primary", use_container_width=True):
                if e in USERS and USERS[e]["pw"]==p:
                    st.session_state.login=e
                    if USERS[e]["plan"]=="paid": st.session_state.unlocked=True
                    st.rerun()
                else: st.error("Invalid")
        with t2:
            st.caption("Name + Email mandatory")
            n=st.text_input("Full Name*", key="s_name"); ne=st.text_input("Email* (report delivery)", key="s_email"); np=st.text_input("Password*", type="password", key="s_pw")
            news=st.checkbox("Subscribe quarterly newsletter", value=True)
            if st.button("Create Account", use_container_width=True):
                if not n or not ne: st.error("Name + Email mandatory!")
                elif ne in USERS: st.error("Exists, login")
                else:
                    USERS[ne]={"pw":np,"name":n,"plan":"free","role":"user","address":"","newsletter":news,"purchases":[],"joined":str(datetime.datetime.now())[:10]}
                    save_all(); st.success("Created! Login now")

if not st.session_state.login:
    st.markdown('<div class="hero"><h1 style="color:white;margin:0;">AI Garden Designer</h1><p>Professional reports + Your affiliate income</p></div>', unsafe_allow_html=True)
    st.info("Login from sidebar")
    st.stop()

# DASHBOARD
if is_admin() and st.session_state.show_dashboard:
    st.markdown('<div class="hero"><h2 style="color:white;margin:0;">📊 Dashboard - Clients Conserved Forever</h2><p>All clients, purchases, addresses, files</p></div>', unsafe_allow_html=True)
    if not SUBS and len([k for k in USERS if USERS[k].get("role")!="admin"])==0:
        st.warning("No clients yet. But new code will now conserve them! Create test client again - this time it will stay after upgrades.")
    import pandas as pd
    if SUBS:
        st.subheader("📋 Jobs (Where you receive client files)")
        df=pd.DataFrame([{"Job#":len(SUBS)-i,"Date":j.get("date"),"Name":j.get("client_name"),"Email":j.get("client_email"),"Home Address":j.get("home_address"),"Service":j.get("service"),"Amount":j.get("amount"),"Status":"PAID" if j.get("paid") else "FREE","Photos":j.get("photo_count"),"Newsletter":j.get("newsletter")} for i,j in enumerate(reversed(SUBS))])
        st.dataframe(df, use_container_width=True)
    if USERS:
        st.subheader("👤 Client Database - Conserved on Upgrades")
        ud=[{"Name":v.get("name"),"Email":k,"Home Address":v.get("address","MISSING"),"Plan":v.get("plan"),"Newsletter":v.get("newsletter"),"Joined":v.get("joined")} for k,v in USERS.items() if v.get("role")!="admin"]
        if ud: st.dataframe(pd.DataFrame(ud), use_container_width=True)
    st.stop()

# CLIENT VIEW
user=USERS[st.session_state.login]
st.markdown(f'<div class="hero"><h3 style="color:white;margin:0;">Welcome {user.get("name")}!</h3><p>Address + Email mandatory for paid precise report</p></div>', unsafe_allow_html=True)

st.markdown("### 📝 Project Details")
c1,c2=st.columns(2)
with c1:
    client_name=st.text_input("Full Name*", value=user.get("name",""))
    client_email=st.text_input("Email* (for delivery)", value=st.session_state.login)
    home_address=st.text_input("Home Address* (mandatory for PAID)", value=user.get("address",""), placeholder="123 Main St, Upper Darby, PA 19082")
with c2:
    zipc=st.text_input("Zip*", value="19082")
    service=st.selectbox("Service & Price - Click to pay instantly*", ["Full Yard Design $49","Removal Plan Only $29","New Planting Only $29","AI Visual Only $19","On-site Consultation $149"])
    newsletter=st.checkbox("Quarterly newsletter (tips + discounts)", value=user.get("newsletter",True))

# INSTANT PAYMENT WHEN PRICE CLICKED - FIX!
amount_map={"Full Yard Design $49":49,"Removal Plan Only $29":29,"New Planting Only $29":29,"AI Visual Only $19":19,"On-site Consultation $149":149}
amt=amount_map.get(service,49)
st.session_state.selected_amount=amt

paid=(user["plan"]=="paid") or st.session_state.unlocked

# SHOW PRICE BOX IMMEDIATELY WHEN SERVICE CLICKED
st.markdown(f'<div class="price-box"><h2 style="margin:0;color:#166534;">{service}</h2><p>You selected: ${amt} - Pay to unlock precise analysis for {home_address or "your address"}</p></div>', unsafe_allow_html=True)

col_pay1,col_pay2=st.columns(2)
with col_pay1:
    if not paid:
        if not home_address or not client_email:
            st.error("⚠️ Enter Home Address + Email to enable payment")
        else:
            st.link_button(f"💳 Pay ${amt} Now - Unlock Report", "https://buy.stripe.com/test_00g5kL2V0", use_container_width=True, type="primary")
            if st.button(f"✅ I Paid ${amt} - Unlock", use_container_width=True):
                USERS[st.session_state.login]["address"]=home_address
                USERS[st.session_state.login]["name"]=client_name
                USERS[st.session_state.login]["newsletter"]=newsletter
                save_all()
                st.session_state.unlocked=True; st.rerun()
    else:
        st.success(f"✅ PAID ${amt} - Unlocked")

notes=st.text_area("What do you want?")
ups=st.file_uploader("📸 Yard Photos", accept_multiple_files=True, type=["jpg","png","jpeg"])

if ups and st.button("✨ Generate & Send to Dashboard", type="primary", use_container_width=True):
    if not client_name or not client_email: st.error("Name + Email mandatory!"); st.stop()
    if paid and not home_address: st.error("Address mandatory for paid!"); st.stop()
    USERS[st.session_state.login]["address"]=home_address; USERS[st.session_state.login]["name"]=client_name; USERS[st.session_state.login]["newsletter"]=newsletter
    job={"client_name":client_name,"client_email":client_email,"home_address":home_address,"zip":zipc,"service":service,"amount":amt if paid else 0,"notes":notes,"date":str(datetime.datetime.now())[:19],"paid":paid,"photo_count":len(ups),"newsletter":newsletter}
    SUBS.append(job)
    if paid: USERS[st.session_state.login]["purchases"].append(job)
    save_all()
    st.balloons(); st.success(f"Saved! Job #{len(SUBS)} - Will be conserved on next upgrades!")
    st.image(ups[0])
