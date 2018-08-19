import argparse
from actions import *
from gitea import GiteaAPI
from gitlab import GitlabAPI, GitlabProjectHook, GitlabProject
import logging

from helpers import save_config, load_config, printlist

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

def config_args():
    parser = argparse.ArgumentParser(
        description="Set up automatic mirroring from GitLab to Gitea in batch",
    allow_abbrev=True,
        epilog="While the Gitlab token is optionnal, the script will fail if the repositories are private"
    )
    parser.add_argument('--personal-token',
                        nargs='?',
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
    parser.add_argument('-c', metavar='file',
                        nargs='?',
                        help='Configuration file',
                        dest='config_file', default=".sync.json",
                        )
    parser.add_argument('-C',
                        help='Disable loading config file',
                        action='store_false',
                        dest='load_config_file', default=".sync.json",
                        )
    parser.add_argument('-r', metavar='regex',
                        nargs='?',
                        help="The full path of repositories will need to match this regex",
                        dest='repo_regex', default="^BdE",
                        )
    parser.add_argument('-S',
                        action='store_true',
                        help='Save command-line arguments to config file',
                        dest='do_save',
                        )
    parser.print_help()
    return parser

if __name__ == '__main__':
    args = config_args().parse_args()
    if args.do_save:
        save_config(args)
    if args.load_config_file:
        load_config(args)

    ga = GitlabAPI(host=args.gitlab_url, personal_token=args.personal_token)
    gt = GiteaAPI(host=args.gitea_url, api_key=args.api_key, personal_token=args.personal_token)
    repos = ga.get_repos()
    gitea_repos = gt.list_repo()
    select_repos(repos, args.repo_regex)
    repos_to_sync = establish_list(gitlab_repos=repos, gitea_repos=gitea_repos)

    already_synced = [repo for repo in repos if repo not in repos_to_sync]
    print("Repositories already synced:")
    show_repos(already_synced)
    brokens = verify_repos(gitea_repos, gt)
    #delete_list(repos=already_synced, gt=gt)
    migrate_list(repos=repos_to_sync, gt=gt)

        #print("testing a gitlab repo's webhooks")
        #show_hooks(ga,59)
    #
        #print("testing gitea owned repos")
        #get_minez(gt)
    #repos, res = ga.get_repos()
    #for repo in repos:
    #    hooks, res = ga.get_hooks(repo.id)
    #    for hook in hooks:
    #        print(hook.__dict__)
