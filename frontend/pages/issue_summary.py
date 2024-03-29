import streamlit as st

from components.sidebar import sidebar
from services.assistant import make_request
from utils.urls import get_username_repo_issues


def issue_summary(title="Issue Summary"):
    sidebar(title)

    st.title(title)

    issue_link = st.text_input(
        "Enter a link to a github issue: (username/reponame/issues/issue_number",
        placeholder="username/reponame/issues/issue_number"
    )
    summarize_btn = st.button("Summarize")

    if summarize_btn:
        with st.spinner():
            issue_path = get_username_repo_issues(issue_link)

            st.write(issue_path, issue_link)

            response = make_request("post", "/summarize", payload={"issue_path": f"/{issue_link}"})
            #
            # response = make_request(
            #         "post", "/summarize", payload={"issue_path": f"/{issue_link}"}
            #     ) if issue_path else None

        if response and response.status_code == 200:
            container = st.container(height=500)

            summary = response.json()['response']

            container.write(summary)
        else:
            st.error("An error occurred. Please make sure the provided url is correct")


issue_summary()
