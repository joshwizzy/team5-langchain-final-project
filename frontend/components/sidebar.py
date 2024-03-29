import os
import requests
import streamlit as st


def sidebar(title="Project"):
    st.sidebar.title(title)
    st.sidebar.page_link("pages/project_issues_chat.py", label="Project Issues")
    st.sidebar.page_link("pages/issue_summary.py", label="Summarize issue")
    st.sidebar.page_link("pages/generate_issue.py", label="Generate issue")
