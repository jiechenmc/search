import os
import sys
import signal
from github import Github
from github import Auth
from github.GithubException import UnknownObjectException
from helper import write_checkpoint, read_checkpoint, save_repo, audit_repo
from multiprocessing import Process


auth = Auth.Token(os.getenv("TOKEN"))

# Public Web Github
g = Github(auth=auth)

# Init Variables
minimum_stars = 100

k8_files = [
    "charts",
    "k8s",
    "manifests",
    "namespace.yaml",
    "deployment.yaml",
    "service.yaml",
]

checkpoint = read_checkpoint(1)


def search_repos(worker_id: int):
    global checkpoint
    repos = g.get_repos(since=checkpoint * worker_id)

    def signal_handler(sig, frame):
        write_checkpoint(checkpoint, worker_id)
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
                # Checking if the git tree has any of the k8 related files
                for file in files:
                    if any(
                        target_filename in file.path for target_filename in k8_files
                    ):
                        print(f"> ✅ {repo_id} {repo_url}")
                        save_repo(repo_url)
                        break

        except Exception:
            # This is a catch all for repositories who has been deleted or has been removed because it violated Github's TOS
            write_checkpoint(checkpoint, worker_id)


if __name__ == "__main__":
    processes = []

    for i in range(1, 11):  # Create 10 processes
        process = Process(target=search_repos, args=(i,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # Wait for all processes to complete

# To close connections after use
g.close()
