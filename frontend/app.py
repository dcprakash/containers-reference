import streamlit as st
import requests

st.title("Simple Message Sender")

message = st.text_input("Enter your message")

if st.button("Send Message"):
    try:
        response = requests.post("http://backend:8080/message", json={"message": message})
        if response.status_code == 200:
            response_data = response.json()
            st.success(f"Response from backend: {response_data['response']}")
        else:
            st.error("Failed to send message")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
