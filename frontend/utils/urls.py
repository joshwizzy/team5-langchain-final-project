import re


def get_username_repo(url):
    # Regular expression pattern to match GitHub usernames and repo names
    pattern = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/?#]+)'

    # Match the pattern in the URL
    match = re.search(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        return f"{username}/{repo_name}"
    else:
        # If the pattern is not matched, try to extract from alternative formats
        alt_pattern = r'([^/]+)/([^/?#]+)'
        alt_match = re.search(alt_pattern, url)
        if alt_match:
            username = alt_match.group(1)
            repo_name = alt_match.group(2)
            return f"{username}/{repo_name}"
        else:
            return None


def get_username_repo_issues(url):
    # Regular expression pattern to match GitHub URLs
    pattern = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)/(?:issues|pullrequests)/(\d+)'

    # Match the pattern in the URL
    match = re.search(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        issue_keyword = "issues" if "issues" in url else "pullrequests"
        issue_number = match.group(3)
        return f"{username}/{repo_name}/{issue_keyword}/{issue_number}"
    else:
        # Try to extract from alternative formats
        alt_pattern = r'([^/]+)/([^/]+)/(issues|pullrequests)/(\d+)'
        alt_match = re.search(alt_pattern, url)
        if alt_match:
            username = alt_match.group(1)
            repo_name = alt_match.group(2)
            issue_keyword = alt_match.group(3)
            issue_number = alt_match.group(4)
            return f"{username}/{repo_name}/{issue_keyword}/{issue_number}"
        else:
            return None
