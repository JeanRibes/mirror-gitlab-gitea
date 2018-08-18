from typing import List

from gitea import GiteaAPI, GiteaRepo
from gitlab import GitlabAPI, GitlabProject


def establish_list(gitlab_repos: List[GitlabProject], gitea_repos: List[GiteaRepo]) -> List[GitlabProject]:
    gitea_names = [repo.name for repo in gitea_repos] #list of the names of gitea synced repos
    return [ labRepo for labRepo in gitlab_repos if labRepo.gitea_name not in gitea_names]

def fix_mirrors(gitea_repos: List[GiteaRepo]):
    non_mirrors = [repo for repo in gitea_repos if repo.mirror==False]

def migrate_list(repos: List[GitlabProject], gt: GiteaAPI):
    for repo in repos:
        print("Migrating "+repo.path_with_namespace)
        gt.mirror_repo(clone_addr=repo.http_url_to_repo,
                       repo_name=repo.gitea_name)