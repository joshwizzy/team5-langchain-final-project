import os
from distutils.util import strtobool

import yaml
import requests
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv, find_dotenv
from yaml.loader import SafeLoader

from components.sidebar import sidebar
from services.assistant import make_request

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


def launch_app(authenticator=None):
    col1, col2 = st.columns((1, 4))

    col1.image("./images/logo.jpeg", width=100)
    col2.title("Github PM Assistant")
    st.markdown(
        """
        ### Streamline your project workflow with Github PM Assistant 👋 :
        """
    )
    st.page_link(
        "pages/project_issues_chat.py",
        label="Ask questions  and get answers about project issues using our intuitive chat interface.  ",
        icon="1️⃣",
    )
    st.page_link(
        "pages/issue_summary.py",
        label="Get concise summaries of Github issues, saving you valuable time.",
        icon="2️⃣",
    )
    st.page_link(
        "pages/generate_issue.py",
        label="Describe features in natural language and instantly generate new Github issues, streamlining your development process.",
        icon="3️⃣",
    )

    if authenticator is not None:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')

    status()
    sidebar()


def status():
    with st.spinner("Checking if API reachable..."):
        try:
            response = make_request("get", "/healthz")
        except requests.exceptions.ConnectionError:
            st.error("API Unreachable")
            return

        if response.status_code == 200:
            st.success("Healthy")
        else:
            st.error("API Unreachable")


def get_authenticator():
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator


def check_auth(authenticator):
    if st.session_state["authentication_status"]:
        return True

    authenticator.login()

    if st.session_state["authentication_status"]:
        return True
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

    return False


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)

    disable_auth = strtobool(os.environ.get("DISABLE_AUTHENTICATION", True))
    if disable_auth:
        launch_app()
        st.stop()

    authenticator = get_authenticator()
    authenticated = check_auth(authenticator)
    if authenticated:
        launch_app(authenticator)
