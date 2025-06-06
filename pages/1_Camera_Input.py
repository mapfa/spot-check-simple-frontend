import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_cropper import st_cropper
from PIL import Image
from io import BytesIO

load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT")

# Initialize session state for tracking the current step
if 'camera_step' not in st.session_state:
    st.session_state.camera_step = 'camera'  # 'camera' or 'crop'
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None

st.title("Spotcheck AI - Camera Input")

# Step 1: Camera Input
if st.session_state.camera_step == 'camera':
    enable = st.checkbox("Enable camera to take a picture of skin area to be checked", value=False)
    picture = st.camera_input("Take a picture", disabled=not enable)
    
    if picture:
        st.session_state.captured_image = picture
        st.session_state.camera_step = 'crop'
        st.rerun()

# Step 2: Image Cropping
elif st.session_state.camera_step == 'crop':
    if st.session_state.captured_image:
        st.write("Crop your image to focus on the area of interest")
        img = Image.open(st.session_state.captured_image)
        cropped_img = st_cropper(img)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Take another picture"):
                st.session_state.camera_step = 'camera'
                st.session_state.captured_image = None
                st.rerun()
        
        with col2:
            if st.button("Scan for malignant spots"):
                # Convert PIL Image to bytes
                img_byte_arr = BytesIO()
                cropped_img.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                files = {'file': img_byte_arr}
                headers = {
                    'accept': 'application/json'
                }
                r = requests.post(API_ENDPOINT, files=files, headers=headers, timeout=60)
                if r.status_code == 200:
                    if r.json()['predicted_class'] == 1:
                        st.badge(f"Malignant spot detected with {round(r.json()['confidence']*100, 2)}% confidence", icon=":material/warning:", color="orange")
                    else:
                        st.badge(f"No malignant spots detected with {round(r.json()['confidence']*100, 2)}% confidence", icon=":material/check:", color="green")
                else:
                    st.write("Error during scan. Please try again later.")
                    st.write(f"Status code: {r.status_code}")
                    st.write(f"Response: {r.text}")