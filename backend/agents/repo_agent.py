import os
from git import Repo

CLONE_DIR = "cloned_repos"


def clone_repository(repo_url: str):
    """
    Clones a GitHub repo and returns local path
    """

    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    local_path = os.path.join(CLONE_DIR, repo_name)

    # remove old clone if exists
    if os.path.exists(local_path):
        import shutil
        shutil.rmtree(local_path)

    Repo.clone_from(repo_url, local_path)

    return local_path
