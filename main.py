import os
import signal
import sys
from github import Github
from github import Auth
from github.GithubException import UnknownObjectException
from helper import write_checkpoint, read_checkpoint, save_repo, audit_repo


auth = Auth.Token(os.getenv("TOKEN"))

# Public Web Github
g = Github(auth=auth)

# Init Variables
checkpoint = read_checkpoint()
minimum_stars = 100

k8_files = [
    "charts",
    "k8s",
    "manifests",
    "namespace.yaml",
    "deployment.yaml",
    "service.yaml",
]


repos = g.get_repos(since=checkpoint)


def signal_handler(sig, frame):
    write_checkpoint(checkpoint)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

for repo in repos:
    repo_id = repo.id
    repo_url = repo.html_url
    checkpoint = repo_id
    print(g.get_rate_limit())
    try:
        if repo.size and repo.stargazers_count >= minimum_stars:
            print(f"> ⭐ {repo_id} {repo_url}")
            audit_repo(repo_url)
            try:
                files = repo.get_git_tree("main", True).tree
            except UnknownObjectException:
                files = repo.get_git_tree("master", True).tree

            if any(file.path in k8_files for file in files):
                print(f"> ✅ {repo_id} {repo_url}")
                save_repo(repo_url)
                continue

    except Exception:
        # This is a catch all for repositories who has been deleted or has been removed because it violated Github's TOS
        write_checkpoint(checkpoint)

# To close connections after use
g.close()
