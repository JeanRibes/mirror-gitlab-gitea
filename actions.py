from typing import List

from gitea import GiteaAPI, GiteaRepo
from gitlab import GitlabAPI, GitlabProject
from sys import stdout
from logging import getLogger
import re
logger = getLogger()

def establish_list(gitlab_repos: List[GitlabProject], gitea_repos: List[GiteaRepo]) -> List[GitlabProject]:
    gitea_names = [repo.name for repo in gitea_repos] #list of the names of gitea synced repos
    return [ labRepo for labRepo in gitlab_repos if labRepo.gitea_name not in gitea_names]

def fix_mirrors(gitea_repos: List[GiteaRepo]):
    non_mirrors = [repo for repo in gitea_repos if repo.mirror==False]

def migrate_list(repos: List[GitlabProject], gt: GiteaAPI):
    print("Migrating projects to Gitea") if len(repos)>0 else None
    i,max=1,len(repos)
    for repo in repos:
        stdout.write("({}/{}) Migrating {}".format(i,max,repo.path_with_namespace))
        stdout.flush()
        response = gt.mirror_repo(clone_addr=repo.clone_addr(personal_token=gt.personal_token),
                       repo_name=repo.gitea_name, private=repo.private)
        print("\r{}({}/{}) Migrated  {}   ".format("[Failed]" if response == False else '',
                                                  i,max,
                                      repo.path_with_namespace))
        i+=1
def delete_list(repos: List[GiteaRepo], gt: GiteaAPI):
    print("Deleting repositories from Gitea")
    i,max=1,len(repos)
    for repo in repos:
        stdout.write("({}/{}) Deleting ".format(i,max)+repo.gitlab_name) #pour print sans saut à la ligne
        stdout.flush()
        response = gt.delete_repo(repo.name)
        print("\r{}({}/{}) Deleted  {}".format("[Failed]" if response==False else '',
                                              i,max,
                                      repo.gitlab_name))
        i+=1

def convert_gitlab_gitea(gitlab: List[GitlabProject], gitea:List[GiteaRepo])->List[GiteaRepo]:
    gitlab_names = [repo.name for repo in gitlab]
    return [repo for repo in gitea if repo.gitlab_name in gitlab_names]

def verify_repos(repos: List[GiteaRepo])->List[GiteaRepo]:
    sync_broken = [r for r in repos if not r.mirror]
    if len(sync_broken)>0:
        logger.warning("Some repositories on Gitea are not mirroring their Gitlab counterpart")
        for r in sync_broken:
            logger.warning("   {} is missing mirror flag".format(r.name))
    return sync_broken

def select_repos(repos: List[GitlabProject], regex: str):
    """
    supprime de la liste les repos qui ne corresponent pas à la regex
    :param repos:
    :param regex:
    :return:
    """
    print("These repositories will not be synced :")
    condition = re.compile(regex) #on compile la regex avant pour de meilleur perfs
    for repo in repos:
        if not condition.match(repo.path_with_namespace):
            print("   {} does not match {}".format(repo.path_with_namespace, regex))
            repos.remove(repo)