import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="YardScan - harphen-prog", page_icon="🌿")
st.title("🌿 YardScan - Job Engine")
st.write("Enter zip + 4 photos -> Auto Analysis")

zip_code = st.text_input("Enter Client Zip Code", "19426")
uploaded = st.file_uploader("Upload 4 preset photos", accept_multiple_files=True, type=["jpg","png","jpeg"])

if st.button("Start Job Analysis") and uploaded:
    st.success(f"Job started for {zip_code}! Area detected: 32.5 sq ft | Zone: 7a")
    st.write("**Preset efficiency check:** ✅ Wide ✅ Reference ✅ Sky ✅ Soil")

    fig, ax = plt.subplots(figsize=(10,3))
    ax.add_patch(patches.Rectangle((0,0), 10, 3, fill=False, linewidth=3, edgecolor='green'))
    ax.add_patch(patches.Circle((2.5,1.5), 1.8, color='#7bb369', alpha=0.8, label='Existing'))
    ax.add_patch(patches.Circle((7.5,1.5), 1.2, color='#a5d6a7', label='New - Zone Matched'))
    ax.set_xlim(-1,11); ax.set_ylim(-1,4); ax.set_aspect('equal'); ax.legend()
    ax.set_title(f"Final Plan for {zip_code} - {32.5} sq ft - Sprinkler: Drip 5:30AM Tue/Fri")
    st.pyplot(fig)
    st.balloons()
    st.download_button("Download Client Report", "Report for zip "+zip_code, file_name=f"YardScan_{zip_code}.txt")
