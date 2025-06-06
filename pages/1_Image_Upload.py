import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT")

st.title("Spotcheck AI - Image Upload")

uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    if st.button("Scan for malignant spots"):
        st.write("Scanning for malignant spots... Please wait.")
        files = {'file': uploaded_file.getvalue()}
        headers = {
            'accept': 'application/json'
        }
        r = requests.post(API_ENDPOINT, files=files, headers=headers, timeout=60)
        if r.status_code == 200:
            st.write("Scan completed. Here are the results:")
            st.write(r.text)
        else:
            st.write("Error during scan. Please try again later.")
            st.write(f"Status code: {r.status_code}")
            st.write(f"Response: {r.text}") 