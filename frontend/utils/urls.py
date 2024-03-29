import re


def get_username_repo(url):
    # Define regular expression pattern to match GitHub URLs
    pattern = r'(?:https?://)?(?:www\.)?(?:github\.com/)?/?(\w+)/(\w+)(?:/.*)?'

    # Search for username and repo name in the URL using regular expression
    match = re.search(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        return f"{username}/{repo_name}"
    else:
        return None


def get_username_repo_issues(url):
    # Define regular expression pattern to match GitHub URLs with issues
    pattern = r'(?:https?://)?(?:www\.)?(?:github\.com/)?/?(\w+)/(\w+)/(?:issues/(\d+))'

    # Search for username, repo name, and issue number in the URL using regular expression
    match = re.search(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        issue_number = match.group(3)
        return f"{username}/{repo_name}/issues/{issue_number}"
    else:
        return None
