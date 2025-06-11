import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_cropper import st_cropper
from PIL import Image
from io import BytesIO

# Set page configuration for wide layout
st.set_page_config(
    page_title="SkinCheckAI - Camera Input",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the menu button and footer
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: rgb(255, 75, 75);
    }
    section[data-testid="stSidebar"] > div {
        color: white !important;
        font-weight: bold !important;
    }
    /* Style all buttons */
    .stButton > button {
        background-color: rgb(255, 75, 75) !important;
        color: white !important;
    }
    .stButton > button:hover {
        background-color: rgb(235, 55, 55) !important;
        border-color: rgb(235, 55, 55) !important;
    }
    .stButton > button:active {
        background-color: rgb(215, 35, 35) !important;
        border-color: rgb(215, 35, 35) !important;
    }
    /* Style secondary buttons differently */
    .stButton > button[kind="secondary"] {
        background-color: white !important;
        color: rgb(255, 75, 75) !important;
        border: 1px solid rgb(255, 75, 75) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: rgba(255, 75, 75, 0.1) !important;
        border-color: rgb(235, 55, 55) !important;
        color: rgb(235, 55, 55) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .st-emotion-cache-16txtl3 {
        color: white !important;
    }
    .st-emotion-cache-16idsys p {
        color: white !important;
    }
    .st-emotion-cache-16idsys {
        color: white !important;
    }
    [data-testid="stSidebarNav"] {
        color: white !important;
    }
    [data-testid="stSidebarNav"] * {
        color: white !important;
    }
    div[data-testid="stSidebarNav"] a {
        color: white !important;
    }
    div[data-testid="stSidebarNav"] span {
        color: white !important;
    }
    button[kind="secondary"] {
        color: white !important;
    }
    .st-emotion-cache-pkbazv {
        color: white !important;
    }
    .st-emotion-cache-1inwz65 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()
API_ENDPOINT = os.getenv("API_URL")

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
        
        # Create columns for the main content area
        main_col1, main_col2 = st.columns([0.2, 0.8])
        
        with main_col1:
            if st.button("Take another picture"):
                st.session_state.camera_step = 'camera'
                st.session_state.captured_image = None
                st.rerun()
            
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
                st.session_state.scan_result = r if r.status_code == 200 else None
                st.session_state.scan_error = None if r.status_code == 200 else {
                    'status_code': r.status_code,
                    'text': r.text
                }
                st.rerun()

        with main_col2:
            if 'scan_result' not in st.session_state:
                st.session_state.scan_result = None
                st.session_state.scan_error = None

            

            # Show results if available
            if st.session_state.scan_result:
                st.markdown("""
                <style>
                .full-width {
                    width: 100%;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }
                .malignant {
                    background-color: #FFF0E6;
                    border: 2px solid #FF6B2C;
                }
                .non-malignant {
                    background-color: #E5FFE5;
                    border: 2px solid #008000;
                }
                </style>
                """, unsafe_allow_html=True)
                
                r = st.session_state.scan_result
                if r.json()['predicted_class'] == 1:
                    confidence = round(r.json()['confidence']*100, 2)
                    st.markdown(
                        f"""
                        <div class="full-width malignant">
                            <h2 style='color: #FF6B2C; margin:0;'>MALIGNANT SPOT DETECTED</h2>
                            <p style='font-size: 20px; margin: 10px 0;'>Confidence: {confidence}%</p>
                            <p style='color: #FF6B2C;'>This mole shows features that may be associated with melanoma or another type of skin cancer, according to our AI model. Please consult a healthcare professional for further evaluation.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    confidence = round(r.json()['confidence']*100, 2)
                    st.markdown(
                        f"""
                        <div class="full-width non-malignant">
                            <h2 style='color: #008000; margin:0;'>NO MALIGNANT SPOTS DETECTED</h2>
                            <p style='font-size: 20px; margin: 10px 0;'>Confidence: {confidence}%</p>
                            <p style='color: #008000;'>Based on the photo you provided, this mole appears benign. It does not currently show visual features commonly associated with skin cancer, according to our AI model.Regular skin checks are still recommended.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            elif st.session_state.scan_error:
                error = st.session_state.scan_error
                st.error("Error during scan. Please try again later.")
                st.write(f"Status code: {error['status_code']}")
                st.write(f"Response: {error['text']}")