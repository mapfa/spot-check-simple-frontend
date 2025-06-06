import streamlit as st
import requests

st.title("Spotcheck AI - Image Upload")

uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image")
    if st.button("Scan for malignant spots"):
        st.write("Scanning for malignant spots... Please wait.")
        url = 'https://model-inference-api-521423942017.europe-west1.run.app/predict'
        files = {'file': uploaded_file.getvalue()}
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