from gitlab import GitlabAPI, GitlabProjectHook


def show_repos(ga):
    repos = ga.get_repos()
    for repo in repos:
        print("[PROJECT]" + str(repo.__dict__))

def show_hooks(ga, repo_id):
    hooks = ga.get_hooks(repo_id)
    for hook in hooks:
        print("[HOOK]" + str(hook.__dict__))


if __name__ == '__main__':
    ga= GitlabAPI(host="https://git.bde-insa-lyon.fr", personal_token='dANDcrXWDEGXJxe3xYUA')
    print(ga.api.headers)
    #show_repos(ga)
    show_hooks(ga,59)
    #repos, res = ga.get_repos()
    #for repo in repos:
    #    hooks, res = ga.get_hooks(repo.id)
    #    for hook in hooks:
    #        print(hook.__dict__)
