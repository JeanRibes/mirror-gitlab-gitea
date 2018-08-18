from typing import List

from gitea import GiteaAPI
from gitlab import GitlabAPI, GitlabProject


def establish_list(gitlab_repos: List[GitlabProject], gitea: GiteaAPI) -> List[GitlabProject]:
    gitea_repos = gitea.list_repo("BdE-Backup")
    gitea_names = [repo.name for repo in gitea_repos] #list of the names of gitea synced repos
    return [ labRepo for labRepo in gitlab_repos if labRepo.gitea_name not in gitea_names]