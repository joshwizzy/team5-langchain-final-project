import os


from dotenv import load_dotenv, find_dotenv
import requests
import streamlit as st


def launch_app():
    print("launching app")
    st.title("Github Issues PM Assistant")

    with st.spinner("Searching for an answer..."):
        api_url = os.environ["API_URL"]
        response = requests.get(f"{api_url}/healthz")
        if response.status_code == 200:
            st.info("Healthy")
        else:
            st.info("API Unreachable")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    launch_app()
