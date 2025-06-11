import streamlit as st

st.set_page_config(
    page_title="SkinCheckAI - Home",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"  # This will hide the menu by default
)

# Hide the menu button and footer
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-text {
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    [data-testid="stSidebar"] {
        background-color: rgb(255, 75, 75);
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
    .nav-icon {
        font-size: 48px;
        color: rgb(255, 75, 75);
        margin-bottom: 10px;
    }
    .button-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }
    .material-icons {
        font-size: 32px !important;
    }
    .custom-button {
        background-color: rgb(255, 75, 75);
        border: none;
        color: white;
        padding: 15px 20px;
        border-radius: 4px;
        cursor: pointer;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        transition: background-color 0.3s;
        text-decoration: none !important;
    }
    .custom-button:hover {
        background-color: rgb(235, 55, 55);
        color: white;
        text-decoration: none !important;
    }
    .custom-button:visited {
        color: white;
        text-decoration: none !important;
    }
    .custom-button .material-icons {
        font-size: 32px;
        color: white;
    }
    .custom-button .button-text {
        font-size: 16px;
        font-weight: 500;
        color: white;
    }
    /* Hide default streamlit button */
    [data-testid="stButton"] {
        display: none;
    }
    /* Style file uploader button */
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
    /* Style file uploader text */
    .uploadedFile {
        color: rgb(255, 75, 75) !important;
    }
    .header-bar {
        background-color: rgba(255, 75, 75, 0.25);
        padding: 1rem 2rem;
        margin: -6rem -4rem 2rem -4rem;
        border-bottom: 1px solid rgba(255, 75, 75, 0.4);
        height: 4rem;
    }
    .header-bar h1 {
        margin: 0;
        color: rgb(49, 51, 63);
        font-weight: 700;
    }
</style>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# Initialize session state for popup
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'next_page' not in st.session_state:
    st.session_state.next_page = None

def show_popup(page):
    st.session_state.show_popup = True
    st.session_state.next_page = page

# Display popup if triggered
if st.session_state.show_popup:
    with st.container():
        st.markdown(f"""
            <style>
                div.stButton button {{
                    z-index: 1002;
                    position: relative;
                }}
                [data-modal-container='true'] {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.5);
                    z-index: 1000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                [data-modal='true'] {{
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    width: 90%;
                    max-width: 600px;
                    margin: 2rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .button-container {{
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                    margin-top: 2rem;
                }}
            </style>
            <div data-modal-container='true'>
                <div data-modal='true'>
                    <h2 style='color: #721c24; margin-bottom: 1rem;'>❗️Important Medical Disclaimer</h2>
                    <div style='margin-bottom: 1.5rem;'>
                        Before proceeding, please acknowledge the following:
                        <ol style='margin-top: 1rem;'>
                            <li>This AI tool is for preliminary screening purposes only.</li>
                            <li>It is not a substitute for professional medical diagnosis.</li>
                            <li>The results should not be used for self-diagnosis.</li>
                            <li>Always consult a qualified healthcare professional for proper diagnosis.</li>
                            <li>If you have concerns about a skin lesion, seek immediate medical attention.</li>
                        </ol>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        ## hardcoded break for button
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        # Add buttons below the popup
        col1, col2, col3 = st.columns([1.67, 1, 1])
        with col2:
            if st.button("I Understand", type="primary", key="understand_btn"):
                st.session_state.show_popup = False
                st.switch_page(f"pages/{st.session_state.next_page}.py")

st.markdown("""
<div class="header-bar"></div>
""", unsafe_allow_html=True)

st.title("Welcome to SkinCheckAI!")

st.markdown("""
<div class='main-text'>
    <h3>Your early warning for skin cancer. Anytime. Anywhere.</h3>
    <p style="margin-top: -0.5rem;">
        SkinCheckAI uses advanced AI technology to help you assess suspicious skin lesions in seconds.
    </p>
    <p>Choose one of the following options to get started:</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <a href="/Camera_Input" target="_self" class="custom-button" style="text-decoration: none;">
            <i class="material-icons">photo_camera</i>
            <span class="button-text">Camera Input</span>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="Image_Upload" target="_self" class="custom-button" style="text-decoration: none;">
            <i class="material-icons">image</i>
            <span class="button-text">Image Upload</span>
        </a>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### How it works:
1. Choose your preferred method of image input (camera or file upload)
2. Follow the instructions to capture or upload your image
3. Use the cropping tool to focus on the area of interest
4. Get instant AI-powered analysis of your skin spot

### Important Note:
This tool is designed to assist in preliminary skin checks only. It is not a replacement for professional medical advice. 
Always consult a healthcare professional for proper diagnosis and treatment.
""")

