import os
import requests
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from components.sidebar import sidebar
from services.assistant import make_request

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


def launch_app():
    st.title("Github PM Assistant")

    status()

    sidebar()


def status():
    with st.spinner("Checking if API reachable..."):
        response = make_request("get", "/healthz")
        if response.status_code == 200:
            st.success("Healthy")
        else:
            st.error("API Unreachable")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    launch_app()
