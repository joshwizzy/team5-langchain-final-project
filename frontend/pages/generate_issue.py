import streamlit as st

from components.sidebar import sidebar
from services.assistant import make_request


def generate_summary(title="Generate Issue"):
    sidebar(title)

    st.title(title)

    feature_description = st.text_input(
        "Enter a feature description:",
    )

    create_issue = st.checkbox("Add the issue to the Github project")
    if create_issue:
        repo_link = st.text_input(
            "Enter a github repo link (username/reponame):",
            placeholder="user_name/repo_name",
        )
        issue_title = st.text_input("Enter a isue title:")

    def generate_issue():
        payload = {"feature_description": feature_description}
        if create_issue:
            payload.update(
                {
                    "create_issue": create_issue,
                    "repo_url": repo_link,
                    "issue_title": issue_title,
                }
            )
        with st.spinner("Generating issue ..."):
            response = make_request("post", "/generate-issue", payload=payload)

        if response.status_code == 200:
            data = response.json()
            if create_issue:
                github_url = data["html_url"]
                st.markdown(
                    f"To view the issue on Github visit [this link]({github_url})."
                )
            st.info("You can copy and paste this issue description on Github")
            st.text(data["response"])
            st.markdown(data["response"])
        else:
            st.error("Failed to generate issue")

    if st.button("Generate Issue"):
        generate_issue()


generate_summary()
