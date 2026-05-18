import streamlit as st
import requests

# API Gateway URL
API_URL = "https://65o388b30k.execute-api.ap-southeast-2.amazonaws.com/dev/rephrase"

st.title("Login Page")

username = st.text_input("UserName")
password = st.text_input("Password", type="password")

if st.button("Submit"):

    payload = {
        "username": username,
        "password": password
    }

    try:

        response = requests.post(API_URL, json=payload)

        result = response.json()

        if result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])

    except Exception as e:
        st.error(f"Error: {e}")