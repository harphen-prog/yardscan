import streamlit as st, json, os, datetime, requests
from urllib.parse import quote

st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* {font-family: 'Inter', sans-serif;}
.hero {background: linear-gradient(135deg, #0f5c36 0%, #22c55e 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 12px;}
.card {background: white; border-radius: 12px; padding: 12px; border: 1px solid #eee; margin-bottom: 8px;}
.price-box {background:#f0fdf4; border:2px solid #22c55e; padding:14px; border-radius:12px; text-align:center;}
</style>
""", unsafe_allow_html=True)

GOOGLE_KEY = st.secrets.get("GOOGLE_MAPS_KEY", "AIzaSyCI4ip2ec-cvsLaV8tLsZzbP8sMQTlngLE")

AFF_FILE = "affiliates.json"
SUB_FILE = "submissions.json"
USER_FILE = "users_db.json"

def load_json(f, default):
    if os.path.exists(f):
        try:
            with open(f) as j:
                d=json.load(j)
                if d: return d
        except: pass
    return default

def save_json(f, data):
    with open(f,"w") as j: json.dump(data,j,indent=2)

AFF = load_json(AFF_FILE, {"Lavender":"https://amazon.com/s?k=lavender","Boxwood":"https://amazon.com/s?k=boxwood"})
SUBS = load_json(SUB_FILE, [])
DEFAULT_USERS = {"harphen-prog@gmail.com":{"pw":"admin123","name":"Harphen Admin","plan":"paid","role":"admin","address":"Upper Darby, PA","newsletter":False,"purchases":[],"joined":"2026-01-01"}}
USERS = load_json(USER_FILE, DEFAULT_USERS)
USERS["harphen-prog@gmail.com"]=DEFAULT_USERS["harphen-prog@gmail.com"]

if "login" not in st.session_state: st.session_state.login=None
if "unlocked" not in st.session_state: st.session_state.unlocked=False
if "show_dashboard" not in st.session_state: st.session_state.show_dashboard=False
if "lat" not in st.session_state: st.session_state.lat=None
if "lng" not in st.session_state: st.session_state.lng=None
if "property_confirmed" not in st.session_state: st.session_state.property_confirmed=False

def is_admin(): return st.session_state.login and USERS.get(st.session_state.login,{}).get("role")=="admin"
def save_all(): save_json(SUB_FILE, SUBS); save_json(USER_FILE, USERS); save_json(AFF_FILE, AFF)

with st.sidebar:
    st.title("🌿 YardScan Pro")
    if st.session_state.login:
        u = USERS.get(st.session_state.login, {})
        st.success(f"{u.get('name','')}")
        st.caption(f"{u.get('plan','free').upper()} PLAN")
        if st.button("Logout", use_container_width=True):
            st.session_state.login=None; st.session_state.unlocked=False; st.session_state.show_dashboard=False; st.rerun()
        if is_admin():
            st.divider()
            st.metric("Clients", len([k for k,v in USERS.items() if v.get("role")!="admin"]))
            st.metric("Jobs", len(SUBS))
            st.metric("Revenue", f"${sum(s.get('amount',0) for s in SUBS)}")
            if st.button("📥 Open Dashboard", type="primary", use_container_width=True):
                st.session_state.show_dashboard=True; st.rerun()
            if st.button("🧑‍🌾 Designer", use_container_width=True):
                st.session_state.show_dashboard=False; st.rerun()
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
            n=st.text_input("Full Name*", key="s_name"); ne=st.text_input("Email*", key="s_email"); np=st.text_input("Password*", type="password", key="s_pw")
            if st.button("Create Account", use_container_width=True):
                if ne in USERS: st.error("Exists")
                else:
                    USERS[ne]={"pw":np,"name":n,"plan":"free","role":"user","address":"","newsletter":True,"purchases":[],"joined":str(datetime.datetime.now())[:10]}
                    save_all(); st.success("Created! Login now")

if not st.session_state.login:
    st.markdown('<div class="hero"><h1 style="color:white;margin:0;">AI Garden Designer</h1></div>', unsafe_allow_html=True)
    st.info("Login from sidebar"); st.stop()

if is_admin() and st.session_state.show_dashboard:
    st.markdown('<div class="hero"><h2 style="color:white;margin:0;">📊 Dashboard</h2></div>', unsafe_allow_html=True)
    import pandas as pd
    if SUBS:
        df=pd.DataFrame(SUBS)
        st.dataframe(df, use_container_width=True)
    st.stop()

user=USERS[st.session_state.login]
st.markdown(f'<div class="hero"><h3 style="color:white;margin:0;">Welcome {user.get("name")} 🌿</h3><p>Address -> Property Map -> Photos</p></div>', unsafe_allow_html=True)

step = 2 if st.session_state.lat and not st.session_state.property_confirmed else 3 if st.session_state.property_confirmed else 1
st.progress(step/3, text=f"Step {step}/3")

st.markdown("### 📝 Step 1: Project Details")
c1,c2=st.columns(2)
with c1:
    client_name=st.text_input("Full Name*", value=user.get("name",""))
    client_email=st.text_input("Email*", value=st.session_state.login)
    home_address=st.text_input("Home Address*", value=user.get("address",""), placeholder="123 Main St, Upper Darby, PA 19082")
with c2:
    zipc=st.text_input("Zip Code*", value="19082")
    service=st.selectbox("Service & Price*", ["Full Yard Design $49","Removal Plan Only $29","New Planting Only $29"])
    newsletter=st.checkbox("Newsletter", value=True)

amount_map={"Full Yard Design $49":49,"Removal Plan Only $29":29,"New Planting Only $29":29}
amt=amount_map.get(service,49)
paid=(user["plan"]=="paid") or st.session_state.unlocked

st.divider()
st.markdown("### 🛰️ Step 2: Property Map - Satellite + Property Line")
if st.button("🔍 Find Property on Satellite", type="primary"):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={quote(home_address)}&key={GOOGLE_KEY}"
    r = requests.get(url, timeout=10).json()
    if r['status'] == 'OK':
        loc = r['results'][0]['geometry']['location']
        st.session_state.lat = loc['lat']
        st.session_state.lng = loc['lng']
        st.session_state.formatted_address = r['results'][0]['formatted_address']
        st.session_state.property_confirmed=False
    else:
        st.error(f"Google Error: {r['status']}")

if st.session_state.lat:
    lat=st.session_state.lat; lng=st.session_state.lng
    map_html = f"""
    <div id="map" style="height:520px;width:100%;border-radius:12px;border:2px solid #22c55e"></div>
    <div style="margin-top:8px;font-family:sans-serif;background:#f0fdf4;padding:8px;border-radius:8px">
      <span id="info">📏 Drag yellow dots to match property line</span>
    </div>
    <script>
    let poly;
    function initMap(){{
      const center={{lat:{lat}, lng:{lng}}};
      const map=new google.maps.Map(document.getElementById('map'),{{zoom:19, center:center, mapTypeId:'satellite'}});
      const o=0.00022;
      const bounds=[{{lat:center.lat+o,lng:center.lng-o}},{{lat:center.lat+o,lng:center.lng+o}},{{lat:center.lat-o,lng:center.lng+o}},{{lat:center.lat-o,lng:center.lng-o}}];
      poly=new google.maps.Polygon({{paths:bounds, strokeColor:'#FFEB3B', strokeWeight:4, fillColor:'#FFEB3B', fillOpacity:0.35, editable:true, draggable:true, map:map}});
      update();
      google.maps.event.addListener(poly.getPath(),'set_at',update);
      google.maps.event.addListener(poly.getPath(),'insert_at',update);
    }}
    function update(){{
      const area=google.maps.geometry.spherical.computeArea(poly.getPath());
      const sqft=Math.round(area*10.7639);
      document.getElementById('info').innerHTML='📏 Lot: <b>'+sqft.toLocaleString()+' sq ft</b> | Lawn: <b>'+Math.round(sqft*0.65).toLocaleString()+' sq ft</b> | Drag yellow dots';
    }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_KEY}&libraries=geometry&callback=initMap" async defer></script>
    """
    st.components.v1.html(map_html, height=580)
    if st.button("✅ Confirm Property Line", type="primary", use_container_width=True):
        st.session_state.property_confirmed=True; st.rerun()
else:
    st.info("Enter address above then click Find")

if not st.session_state.property_confirmed:
    st.stop()

st.divider()
st.markdown("### 📸 Step 3: Photos + Payment")
st.markdown(f'<div class="price-box"><h3 style="margin:0;color:#166534;">{service} - ${amt}</h3></div>', unsafe_allow_html=True)

if not paid:
    with st.form("pay_form"):
        card=st.text_input("Card Number", placeholder="4242 4242 4242 4242")
        if st.form_submit_button(f"Pay ${amt} Now", type="primary"):
            if len(card)>=8:
                USERS[st.session_state.login]["plan"]="paid"; save_all(); st.session_state.unlocked=True; st.rerun()

notes=st.text_area("What do you want?")
ups=st.file_uploader("📸 Yard Photos", accept_multiple_files=True, type=["jpg","jpeg","png"])

if ups and st.button("✨ Generate & Send to Dashboard", type="primary", use_container_width=True):
    job={"client_name":client_name,"client_email":client_email,"home_address":home_address,"lat":st.session_state.lat,"lng":st.session_state.lng,"service":service,"amount":amt,"notes":notes,"date":str(datetime.datetime.now())[:19],"paid":paid,"photo_count":len(ups)}
    SUBS.append(job); save_all()
    st.balloons(); st.success(f"Saved Job #{len(SUBS)} with property map!")

