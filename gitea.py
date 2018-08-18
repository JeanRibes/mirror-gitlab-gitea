import json
import logging

from simple_rest_client.api import API
from simple_rest_client.exceptions import ServerError
from simple_rest_client.models import Response
from simple_rest_client.resource import Resource

from helpers import ServerAPI, DataModel, get_list
logger = logging.getLogger()

class ReposRessource(Resource):
    actions = {
        'search': {'method': 'GET', 'url': 'repos/search'},  # il faut une query 'q'=recherche
        'migrate': {'method': 'POST', 'url': 'repos/migrate'},
    }


class OrgRessource(Resource):
    actions = {
        'list_repos': {'method': 'GET', 'url': 'orgs/{}/repos'},
        'mines': {'method': 'GET', 'url': 'user/{}/orgs'},  # organisation du username
    }
class MeRessource(Resource):
    actions = {
        'me':{'method':'GET','url':'user'},
        'repos':{'method':'GET','url':'user/repos'}

    }

class GiteaOwner(DataModel):
    id = 2
    login = "BdE-Backup"
    full_name = ""
    email = ""
    avatar_url = "https://git.ribes.me/avatars/2"
    username = "BdE-Backup"


class GiteaRepo(object):
    def __init__(self, owner=None, **kwargs):
        self.__dict__.update(kwargs)
        # print(str(owner))
        self.owner = GiteaOwner(**owner)

    id = 8
    name = "adhesion-frontend"
    full_name = "BdE-Backup/adhesion-frontend"
    description = "frontend unifi&"
    empty = False
    private = False
    fork = False
    parent = None
    mirror = True
    size = 534
    html_url = "https://git.ribes.me/BdE-Backup/adhesion-frontend"
    ssh_url = "git@localhost:BdE-Backup/adhesion-frontend.git"
    clone_url = "https://git.ribes.me/BdE-Backup/adhesion-frontend.git"
    website = ""
    stars_count = 1
    forks_count = 0
    watchers_count = 1
    open_issues_count = 0
    default_branch = "dev"
    created_at = "2018-08-15T17:00:24Z"
    updated_at = "2018-08-16T15:54:56Z"
    @property
    def gitlab_name(self):
        return self.name.replace("_._", '/') #because '/' isn't allowed in Gitea, and there are no namespaces

class GiteaAPI(ServerAPI):
    host = ""

    def __init__(self, host, api_key):
        super().__init__(host)
        self.api = API(api_root_url=self.host + 'api/v1',
                       params={'token': api_key},
                       headers={'Content-Type':'application/json'},
                       timeout=60,
                       json_encode_body=True,
                       append_slash=False)
        self.api.add_resource(resource_name='repos', resource_class=ReposRessource)
        self.api.add_resource(resource_name='orgs', resource_class=OrgRessource)
        self.api.add_resource(resource_name='user', resource_class=MeRessource)

    # def search_repo(self, query, mode='mirror', only_me=True, uid=None):
    #    response = self.api.repos.search(params={'q':query,
    #                                             'uid':uid, #utilisateur
    #                                             'mode':mode, #type de repo : fork, source, mirror, collaborative
    #                                             'exclusive':only_me #uniquement ceux qui appartiennent au user spécifié
    #                                             })
    def list_repo(self):
        response = self.api.user.repos()
        return get_list(response, GiteaRepo)

    def mirror_repo(self, clone_addr, repo_name, desc="Migrated by a script", username=None, password=None, private=True):
        body = {
            "auth_password": password,
            "auth_username": username,
            "clone_addr": clone_addr,
            "description": desc,
            "mirror": True,
            "private": private,
            "repo_name": repo_name,
            "uid": self.api.user.me().body['id']
        }
        try:
            return self.api.repos.migrate(body=body)
        except ServerError:
            logger.exception("Remote authentication might be required to clone this repository")
