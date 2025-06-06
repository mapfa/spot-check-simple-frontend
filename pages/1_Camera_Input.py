import streamlit as st
import requests

st.title("Spotcheck AI - Camera Input")

enable = st.checkbox("Enable camera to take a picture of skin area to be checked", value=False)
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.write("Image has been captured. Now you can send it to scan for malignant spots.")
    if st.button("Scan for malignant spots"):
        st.write("Scanning for malignant spots... Please wait.")
        url = 'https://model-inference-api-521423942017.europe-west1.run.app/predict'
        files = {'file': picture.getvalue()}
        headers = {
            'accept': 'application/json'
        }
        r = requests.post(url, files=files, headers=headers, timeout=60)
        if r.status_code == 200:
            st.write("Scan completed. Here are the results:")
            st.write(r.text)
        else:
            st.write("Error during scan. Please try again later.")
            st.write(f"Status code: {r.status_code}")
            st.write(f"Response: {r.text}") 