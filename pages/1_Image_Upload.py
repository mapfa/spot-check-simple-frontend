import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_cropper import st_cropper
from PIL import Image
from io import BytesIO

load_dotenv()
API_ENDPOINT = os.getenv("API_URL")

# Initialize session state for tracking the current step
if 'upload_step' not in st.session_state:
    st.session_state.upload_step = 'upload'  # 'upload' or 'crop'
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

st.set_page_config(
    page_title="SkinCheckAI - Image Upload",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the menu button and footer
st.markdown("""
<style>
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgb(255, 75, 75);
    }
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebarNav"] *,
    div[data-testid="stSidebarNav"] a,
    div[data-testid="stSidebarNav"] span {
        color: white !important;
    }

    /* Main content layout */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1000px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Center all content blocks */
    div[data-testid="stVerticalBlock"] > div,
    .element-container,
    [data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
        flex-direction: column;
        align-items: center;
    }

    /* Standard button styling */
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

    /* Secondary button styling */
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

    /* File uploader styling */
    .stFileUploader,
    section[data-testid="stFileUploader"] {
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    .stFileUploader > div > div {
        background-color: rgb(255, 75, 75) !important;
        color: white !important;
    }
    .stFileUploader > div > div:hover {
        background-color: rgb(235, 55, 55) !important;
    }
    .uploadedFile {
        text-align: center !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        color: rgb(255, 75, 75) !important;
    }

    /* Image and Cropper styling */
    .stCropper,
    [data-testid="stImage"],
    .streamlit-cropper {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }
    img,
    canvas.react-crop-component {
        display: block !important;
        margin: 0 auto !important;
        max-width: 500px !important;
        height: auto !important;
    }

    /* Text and container styling */
    .instruction-text {
        text-align: center !important;
        width: 100% !important;
        margin: 1rem auto !important;
        max-width: 500px !important;
    }
    .button-container {
        width: 100% !important;
        max-width: 500px !important;
        margin: 1rem auto !important;
        display: flex !important;
        justify-content: center !important;
        gap: 1rem !important;
    }
    .result-message {
        margin: 1rem auto !important;
        max-width: 500px !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Spotcheck AI - Image Upload")

# Create a centered container for all components except title
with st.container():
    # Step 1: Image Upload
    if st.session_state.upload_step == 'upload':
        st.markdown('<div class="instruction-text">Choose an image file to upload</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            st.session_state.uploaded_image = uploaded_file
            st.session_state.upload_step = 'crop'
            st.rerun()

    # Step 2: Image Cropping
    elif st.session_state.upload_step == 'crop':
        if st.session_state.uploaded_image:
            st.markdown('<div class="instruction-text">Crop your image to focus on the area of interest</div>', unsafe_allow_html=True)
            
            # Initialize scan result state if not present
            if 'scan_result' not in st.session_state:
                st.session_state.scan_result = None
                st.session_state.scan_error = None

            # Show the cropper
            img = Image.open(st.session_state.uploaded_image)
            # Resize the image if it's too large
            #max_size = 500
            #if img.size[0] > max_size or img.size[1] > max_size:
                # ratio = min(max_size/img.size[0], max_size/img.size[1])
                # new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
                # img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            cropped_img = st_cropper(
                img,
                realtime_update=True,
                box_color="rgb(255, 75, 75)",
                aspect_ratio=None
            )

            # Add some spacing
            st.write("")

            # Create a centered button container
            button_container = st.container()
            with button_container:
                st.markdown('<div class="button-container">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Scan for malignant spots", use_container_width=True):
                        # Convert PIL Image to bytes
                        img_byte_arr = BytesIO()
                        if cropped_img.mode == 'RGBA':
                            cropped_img = cropped_img.convert('RGB')
                        cropped_img.save(img_byte_arr, format='JPEG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        files = {'file': img_byte_arr}
                        headers = {'accept': 'application/json'}
                        r = requests.post(API_ENDPOINT, files=files, headers=headers, timeout=60)
                        st.session_state.scan_result = r if r.status_code == 200 else None
                        st.session_state.scan_error = None if r.status_code == 200 else {
                            'status_code': r.status_code,
                            'text': r.text
                        }
                        st.rerun()

                with col2:
                    if 'scan_result' in st.session_state and st.session_state.scan_result:
                        if st.button("Upload another image", use_container_width=True):
                            st.session_state.upload_step = 'upload'
                            st.session_state.uploaded_image = None
                            del st.session_state.scan_result
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # Show results if available
            if st.session_state.scan_result:
                r = st.session_state.scan_result
                if r.status_code == 200:
                    confidence = round(r.json()['confidence']*100, 2)
                    if r.json()['predicted_class'] == 1:
                        st.markdown(
                            f"""
                            <div class="result-message" style="
                                background-color: #FFF0E6;
                                border: 2px solid #FF6B2C;
                                padding: 10px;
                                border-radius: 5px;
                            ">
                                <h3 style="color: #FF6B2C; margin: 0;">
                                    ⚠️ Malignant spot detected with {confidence}% confidence
                                </h3>
                                <ul style="color: #FF6B2C; margin: 10px 0 0 0; padding-left: 1.2rem; list-style-position: outside;">
                                    <li>This mole shows features that may be associated with melanoma or another type of skin cancer, according to our AI model.</li>
                                    <li>Please consult a healthcare professional for further evaluation.</li>
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="result-message" style="
                                background-color: #E5FFE5;
                                border: 2px solid #008000;
                                padding: 10px;
                                border-radius: 5px;
                            ">
                                <h3 style="color: #008000; margin: 0;">
                                    ✅ No malignant spots detected with {confidence}% confidence
                                </h3>
                                <ul style="color: #008000; margin: 10px 0 0 0; padding-left: 1.2rem; list-style-position: outside;">
                                    <li>Based on the photo you provided, this mole appears benign </li> 
                                    <li>It does not currently show visual features commonly associated with skin cancer, according to our AI model.</li>
                                    <li>Regular skin checks are still recommended.</li>
                                </ul>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            elif st.session_state.scan_error:
                error = st.session_state.scan_error
                st.error("Error during scan. Please try again later.")
                st.write(f"Status code: {error['status_code']}")
                st.write(f"Response: {error['text']}") 