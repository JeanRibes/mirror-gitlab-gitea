from gitlab import GitlabAPI, GitlabProjectHook


def show_repos(ga):
    repos, response = ga.get_repos()
    for repo in repos:
        print("[PROJECT]" + str(repo.__dict__))

def show_hooks(ga, repo_id):
    hooks = ga.get_hooks(repo_id)
    print("[HOOKS]" + str(hooks))
    for hook in hooks:
        h = GitlabProjectHook(**hook)
        print("[HOOK]" + str(h.__dict__))


if __name__ == '__main__':
    ga= GitlabAPI(host="https://git.bde-insa-lyon.fr", personal_token='')
    show_hooks(ga,52)
    repos, res = ga.get_repos()
    for repo in repos:
        hooks, res = ga.get_hooks(repo.id)
        for hook in hooks:
            print(hook.__dict__)
