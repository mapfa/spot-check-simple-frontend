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
if 'upload_step' not in st.session_state:
    st.session_state.upload_step = 'upload'  # 'upload' or 'crop'
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

st.title("Spotcheck AI - Image Upload")

# Step 1: Image Upload
if st.session_state.upload_step == 'upload':
    uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.upload_step = 'crop'
        st.rerun()

# Step 2: Image Cropping
elif st.session_state.upload_step == 'crop':
    if st.session_state.uploaded_image:
        st.write("Crop your image to focus on the area of interest")
        img = Image.open(st.session_state.uploaded_image)
        cropped_img = st_cropper(img)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Upload another image"):
                st.session_state.upload_step = 'upload'
                st.session_state.uploaded_image = None
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