import argparse
from actions import *
from gitea import GiteaAPI
from gitlab import GitlabAPI, GitlabProjectHook, GitlabProject
import logging


logger = logging.getLogger(__name__)

def show_repos(repos: List[GitlabProject]):
    for repo in repos:
        #print("[PROJECT]" + str(repo.__dict__))
        print("   {} {} {}".format(repo.path_with_namespace, repo.http_url_to_repo, repo.gitea_name))

def show_hooks(ga, repo_id):
    hooks = ga.get_hooks(repo_id)
    for hook in hooks:
        print("[HOOK]" + str(hook.__dict__))

def get_minez(gt):
    repos = gt.list_repo("BdE-Backup")
    for repo in repos:
        #print("[BdE-Backup]"+str(repo.__dict__))
        print("repo {} owned by {} aka {}".format(repo.name, repo.owner.login,
                                                  repo.owner.username))

def config_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set up automatic mirroring from GitLab to Gitea in batch",
    allow_abbrev=True,
        epilog="While the Gitlab token is optionnal, the script will fail if the repositories are private"
    )
    parser.add_argument('--personal-token',
                        metavar='token',
                        help="Your Gitlab personal access token",
                        dest='personal_token')
    parser.add_argument('--api-key',
                        metavar='token',
                        help='Your Gitea api key',
                        dest='api_key')
    parser.add_argument('--gitlab',
                        help='URL of the Gitlab host',
                        metavar='url',
                        dest='gitlab_url')
    parser.add_argument('--gitea',
                        help='URL of the Gitea host',
                        metavar='url',
                        dest='gitea_url')
    parser.add_argument('-r', metavar='regex',
                        nargs='?',
                        help="The full path of repositories will need to match this regex",
                        dest='repo_regex', default="",
                        )
    parser.add_argument('--fix-mirroring', action='store_true',
                        help="Remove and recreate repos that are not in sync, with 'mirror'=false",
                        dest='fix_mirrors')
    args = parser.parse_args()
    if args.api_key and args.gitea_url and args.gitlab_url:
        return args
    else:
        parser.print_help()
        parser.exit(status=1, message="Missing things are missing, exiting\n")

if __name__ == '__main__':
    args = config_args()

    ga = GitlabAPI(host=args.gitlab_url, personal_token=args.personal_token)
    gt = GiteaAPI(host=args.gitea_url, api_key=args.api_key, personal_token=args.personal_token)
    repos = ga.get_repos()
    gitea_repos = gt.list_repo()
    select_repos(repos, args.repo_regex)
    repos_to_sync = establish_list(gitlab_repos=repos, gitea_repos=gitea_repos)

    already_synced = [repo for repo in repos if repo not in repos_to_sync]
    print("Repositories already synced:")
    show_repos(already_synced)
    brokens = verify_repos(gitea_repos)

    if args.fix_mirrors and len(brokens)>0:
        print("Re-creating repos that are not mirroring Gitlab")
        delete_list(repos=brokens, gt=gt)
        migrate_list(
            repos=establish_list(repos,list(set(gitea_repos)-set(brokens))), #'hack' that migrates previously broken repos and missing repos
            gt=gt)
    elif len(brokens)>0:
        print("Some backups are broken, use option '--fix-mirroring' to re-migrate them properly")
    else:
        migrate_list(repos=repos_to_sync, gt=gt)