import requests
import re
import os
import time

# The TOKEN environment variable is the Github Personal Access Token
auth_token = os.getenv("TOKEN")
query = "q=stars:>=100 is:public topic:helm"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {auth_token}",
    "X-GitHub-Api-Version": "2022-11-28",
}
endpoint = f"https://api.github.com/search/repositories?{query}&sort=stars&order=desc&per_page=100&page=1"


while True:
    print(f"-> {endpoint}")
    r = requests.get(endpoint, headers=headers)

    rheaders = r.headers

    rate_limit = int(rheaders["X-RateLimit-Limit"])
    remaining_limit = int(rheaders["X-RateLimit-Remaining"])
    rate_reset = int(rheaders["X-RateLimit-Reset"])
    link_header = rheaders["Link"]

    has_next = "next" in link_header

    if not has_next:
        break

    # Parsing Data
    # example response object: https://api.github.com/repos/matevip/matecloud
    # git_url, html_url may be of interest
    # contrib = [rsp["contributors_url"] for rsp in data] Not sure if the number of contributors is of interest since we filtered by stars

    data = r.json()["items"]
    repo_urls = ["".join([rsp["html_url"], "\n"]) for rsp in data]

    # Write to file

    with open("out.txt", "a+") as f:
        f.writelines(repo_urls)

    # change to next endpoint
    links = link_header.split(",")
    for link in links:
        if "next" in link:
            url = re.search(r"<(.+)>", link).group(1)
            endpoint = url
            break

    if remaining_limit == 0:
        time.sleep(int(rate_reset - time.time()) + 1)
