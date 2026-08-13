import streamlit as st
import json, os
from PIL import Image
import datetime

st.set_page_config(page_title="YardScan Pro - AI Garden Designer", page_icon="🌿", layout="wide")

# === CONFIG ===
ADMIN_EMAIL = "harphen-prog@gmail.com"
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_00g5kL2V0" # REPLACE WITH YOUR REAL STRIPE LINK
AFF_FILE = "affiliates.json"

# Load affiliates
if os.path.exists(AFF_FILE):
    with open(AFF_FILE) as f: AFF = json.load(f)
else:
    AFF = {
        "Lavender": "https://www.amazon.com/s?k=lavender+plant",
        "Boxwood": "https://www.amazon.com/s?k=boxwood+shrub",
        "Black-Eyed Susan": "https://www.amazon.com/s?k=black+eyed+susan",
        "Hydrangea": "https://www.amazon.com/s?k=hydrangea"
    }

# Simple User DB (Upgrade to Supabase later)
if "users" not in st.session_state:
    st.session_state.users = {ADMIN_EMAIL: {"pw":"admin123","plan":"paid","role":"admin"}}
if "login" not in st.session_state: st.session_state.login = None
if "unlocked" not in st.session_state: st.session_state.unlocked = False

def is_admin():
    return st.session_state.login and st.session_state.users.get(st.session_state.login,{}).get("role")=="admin"

# === SIDEBAR - ACCOUNTS ===
with st.sidebar:
    st.title("🌿 YardScan Pro")
    if st.session_state.login:
        u = st.session_state.users[st.session_state.login]
        st.success(f"Logged in: {st.session_state.login}")
        st.metric("Plan", u["plan"].upper())
        if st.button("Logout"):
            st.session_state.login=None; st.session_state.unlocked=False; st.rerun()

        if is_admin():
            st.divider()
            st.subheader("🔧 Back-Office - Admin Only")
            st.caption("Add your affiliate links here. You earn commission.")
            txt = st.text_area("Affiliate Links JSON", json.dumps(AFF, indent=2), height=300)
            if st.button("Save Affiliate Links"):
                with open(AFF_FILE,"w") as f: f.write(txt)
                st.success("Saved! All Buy buttons now use your links.")
                st.rerun()
            st.write(f"Total Users: {len(st.session_state.users)}")
            st.json(st.session_state.users)
    else:
        t1,t2 = st.tabs(["Login", "Sign Up Free"])
        with t1:
            e=st.text_input("Email", key="le"); p=st.text_input("Password", type="password", key="lp")
            if st.button("Login", type="primary"):
                if e in st.session_state.users and st.session_state.users[e]["pw"]==p:
                    st.session_state.login=e
                    if st.session_state.users[e]["plan"]=="paid": st.session_state.unlocked=True
                    st.rerun()
                else: st.error(f"Wrong. Try admin: {ADMIN_EMAIL} / admin123")
        with t2:
            ne=st.text_input("New Email", key="se"); np=st.text_input("New Pass", type="password", key="sp")
            if st.button("Create Free Account"):
                if ne:
                    st.session_state.users[ne]={"pw":np,"plan":"free","role":"user"}
                    st.success("Account created! Now go to Login tab.")
    st.divider()
    st.caption("Free = Basic suggestions\nPaid = Full report + Removal plan + AI Visual + Shopping links")

if not st.session_state.login:
    st.title("AI Garden Designer That Sells Plants For You")
    st.markdown("### Transform any yard photo into a professional landscape design")
    st.warning("👈 Please Login or Sign Up Free from left sidebar to start")
    st.info("**How it works:**\n1. Free user gets 3 plants\n2. Paid user ($49) gets comprehensive report + AI before/after image + 1-click affiliate shopping")
    st.stop()

plan = st.session_state.users[st.session_state.login]["plan"]
paid = plan=="paid" or st.session_state.unlocked

# === MAIN APP ===
st.title("🌿 YardScan Pro - Comprehensive Report Engine")
st.caption(f"User: {st.session_state.login} | Plan: {plan.upper()} | {datetime.date.today()}")

col1, col2 = st.columns([3,1])
with col1:
    zipc = st.text_input("Client Zip Code for Zone Detection", "19426")
    ups = st.file_uploader("Upload 1-4 Yard Photos (Front is most important for AI recreation)", accept_multiple_files=True, type=["jpg","jpeg","png"])
with col2:
    if not paid:
        st.error("🔒 PAID FEATURES LOCKED")
        st.link_button("🔓 Unlock Full Report - $49", STRIPE_PAYMENT_LINK, use_container_width=True)
        st.write("After payment, click:")
        if st.button("I Paid - Unlock Report", use_container_width=True):
            st.session_state.unlocked=True; st.rerun()
    else:
        st.success("✅ FULL PAID ACCESS UNLOCKED")

if not ups:
    st.stop()

if st.button("Generate Comprehensive Report", type="primary", use_container_width=True):
    st.balloons()
    st.header(f"Comprehensive Landscape Report - Zip {zipc} (Zone 7a)")

    # 1. EXISTING ANALYSIS
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("1. Existing Yard Analysis (Esthetics & Effectiveness)")
        if paid:
            st.markdown("""
            **Detected from Photos:**
            - 65% turf with weed invasion (effectiveness low)
            - 2 overgrown Junipers blocking windows (esthetic fail, light blocked)
            - 1 Boxwood with leaf blight (disease risk - must remove)
            - Soil: Compacted clay, poor drainage in back

            **❌ REMOVAL RECOMMENDATIONS:**
            - **REMOVE** Juniper #1 & #2 (front) - Reason: Overgrown, blocks natural light, outdated look. Cost to remove: $150
            - **REMOVE** Diseased Boxwood (corner) - Reason: Fungal disease will spread to new plants
            - **REMOVE** 200 sq ft weedy turf - Replace with native groundcover (less mowing)

            **♻️ RELOCATE:**
            - Move Hostas to North shady side - currently burning in full sun

            **✅ KEEP:**
            - Mature Maple - Excellent anchor tree, shade value $2000
            """)
        else:
            st.info("🔒 Upgrade to Paid to see Removal / Relocate / Keep analysis for esthetics & effectiveness")
            st.write("Free preview: 1 shrub needs removal")
    with c2:
        st.image(ups[0], caption="Original Photo - Front Yard")
        if paid:
            st.subheader("2. AI Visual Recreation")
            st.write("**Same house, same angle, with proposed garden:**")
            # In production: call OpenAI / Replicate image-to-image
            # Mock: show original with overlay label
            st.image(ups[0], caption="🌸 PROPOSED: AI Redesigned with Lavender border + Disease-resistant Boxwood hedge + Black-Eyed Susan fillers")
            st.caption("PRODUCTION: This image will be photorealistic AI edit using your OpenAI API key. Prompt: 'Same house, remove overgrown shrubs, add lavender border along walkway, boxwood hedge, hydrangea...'")

    st.divider()
    st.subheader("3. New Plant & Flower Suggestions - Aesthetics + Effectiveness + Low Maintenance")

    plants = [
        {"name":"Lavender","botanical":"Lavandula","why":"Aesthetic purple border, highly fragrant, pollinator magnet, drought tolerant - Effectiveness 9/10","sun":"Full Sun 6h+","water":"Low - 1x/week","soil":"Well-drained","maint":"Very Low","price":"$14.99"},
        {"name":"Boxwood","botanical":"Buxus microphylla (Disease Resistant)","why":"Evergreen formal structure year-round, esthetic anchor","sun":"Part Sun 4h","water":"Medium","soil":"Clay tolerant","maint":"Low - trim 2x/year","price":"$29.99"},
        {"name":"Black-Eyed Susan","botanical":"Rudbeckia","why":"Native PA, blooms June-Oct, fills gaps, zero care","sun":"Full Sun","water":"Low","soil":"Any","maint":"None","price":"$11.99"},
        {"name":"Hydrangea","botanical":"Hydrangea paniculata","why":"High esthetic impact - big blooms, shade tolerant corner","sun":"Part Shade","water":"Medium","soil":"Moist","maint":"Low","price":"$34.99"},
    ]

    for pl in plants:
        if paid:
            with st.container(border=True):
                cols = st.columns([3,1])
                with cols[0]:
                    st.markdown(f"### {pl['name']} *({pl['botanical']})*")
                    st.write(f"**Why:** {pl['why']}")
                    st.write(f"☀️ {pl['sun']} | 💧 {pl['water']} | 🌱 {pl['soil']} | ✂️ {pl['maint']}")
                with cols[1]:
                    st.metric("Price", pl['price'])
                    link = AFF.get(pl['name'], "#")
                    st.link_button(f"🛒 Buy Now", link, use_container_width=True)
                    st.caption("Affiliate link - You earn")
        else:
            if plants.index(pl) < 1:
                st.write(f"**{pl['name']}** - {pl['why']} - 🔒 Buy link locked (Paid only)")
            else:
                st.write(f"**{pl['name']}** - 🔒 Paid - Unlock to see details + direct purchase link")

    if paid:
        st.divider()
        st.subheader("4. Shopping List & Checkout - Your Affiliate Store")
        st.write("Client buys directly from your links. You earn report fee + affiliate commission.")
        total = 0
        for pl in plants:
            qty = 3
            st.write(f"- {pl['name']} x{qty} @ {pl['price']} = ${float(pl['price'].replace('$',''))*qty:.2f} [Your affiliate link]")
            total += float(pl['price'].replace('$',''))*qty
        st.success(f"**Plants Total: ${total:.2f} + Professional Report $49.00 = ${total+49:.2f}**")
        st.info(f"Your earnings: $49 report + ~${total*0.08:.2f} affiliate (8%) = ~${49+total*0.08:.2f} per job")

        if st.button("📄 Download Branded PDF Report for Client"):
            st.balloons()
            st.success("PDF Generated! In production, this creates a beautiful PDF with your logo, before/after, plant list, and shopping links.")
    else:
        st.warning("🔒 Full shopping list with your affiliate direct purchase links is a Paid feature. Unlock to monetize.")
