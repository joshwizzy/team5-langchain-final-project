import streamlit as st

from components.sidebar import sidebar


def issue_summary(title="Issue Summary"):
    sidebar(title)

    st.title(title)


issue_summary()
