import streamlit as st
st.set_page_config(page_title="YardScan Pro", page_icon="🌿", layout="wide")

if "pics" not in st.session_state: st.session_state.pics=[]

st.title("👑 Admin Dashboard - FIXED UPLOAD")
st.write("File upload only - camera OFF by default")

# ONLY FILE UPLOAD - NO CAMERA INPUT HERE
uploaded = st.file_uploader("Upload Yard Pictures (1-3) - Choose from file", type=["jpg","jpeg","png"], accept_multiple_files=True, key="fixed_uploader")

if uploaded:
    st.session_state.pics = uploaded
    st.success(f"✅ {len(uploaded)} file(s) loaded!")
    for p in uploaded:
        st.image(p, width=300)
    st.balloons()

# Camera only if user wants it - no auto start
show_cam = st.checkbox("I want to use camera")
if show_cam:
    cam = st.camera_input("Take Photo Now")
    if cam:
        st.session_state.pics = [cam]
        st.image(cam, width=300)

if st.session_state.pics:
    if st.button("✅ Execute / OK - Analyze Yard", type="primary", use_container_width=True):
        st.success("Analyzing...")
        st.image(st.session_state.pics[0], caption="Your Yard")
else:
    st.info("Select files above - preview will show here")
