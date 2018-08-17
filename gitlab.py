import logging

from simple_rest_client.api import API
from simple_rest_client.exceptions import AuthError
from simple_rest_client.resource import Resource

from helpers import get_list, DataModel

logger = logging.getLogger('gitlab')
class HookRessource(Resource):
    actions = {
        'list': {'method': 'GET', 'url': 'projects/{}/hooks'},
        'retrieve': {'method': 'GET', 'url': 'projects/{}/hooks/{}'},
        'create': {'method': 'POST', 'url': 'projects/{}/hooks'},
    }
class GitlabAPI(object):
    host = ""
    def __init__(self, host, personal_token=None, oauth_token=None):
        self.host = host
        assert host is not None, "Define a base URL for the Gitlab Server"
        if not self.host.endswith('/'):
            self.host += ''
        self.api = API(api_root_url=self.host+'/api/v4',
                       headers={'Private-Token':personal_token} if personal_token is not None else
                       {'Authorization':'Bearer '+oauth_token} if oauth_token is not None else None,
                       timeout=60,
                       json_encode_body=True,
                       append_slash=False)

        self.api.add_resource(resource_name='projects')
        self.api.add_resource(resource_name='hooks', resource_class=HookRessource)
        print(self.api.projects.actions)
        print(self.api.hooks.actions)

    def create_hook(self, project_id, webhook_url):
        self.api.hooks.create(project_id, body=GitlabProjectHook(id=project_id,
                                                                          url=webhook_url,
                                                                          token=''))
    def get_hooks(self, project_id):
        try:
            response = self.api.hooks.list(project_id)
            return get_list(response, GitlabProjectHook)
        except AuthError as e:
            logger.exception("Erreur d'accès à la ressource")
            return []

    def get_repos(self):
        response = self.api.projects.list()
        return get_list(response, GitlabProject)

class GitlabProject(DataModel):
    """
    'model' of a Gilab project response with only the interesting fields
    """
    id = 0
    description = ''
    default_branch = "master"
    visibility = "public",
    ssh_url_to_repo = "git@example.com:diaspora/diaspora-project-site.git",
    http_url_to_repo = "http://example.com/diaspora/diaspora-project-site.git",
    name = "Diaspora Project Site",
    path =  "diaspora-project-site",
    path_with_namespace = "diaspora/diaspora-project-site",
    created_at = "2013-09-30T13:46:02Z",
    last_activity_at = "2013-09-30T13:46:02Z",
    creator_id = 3,

class GitlabProjectHook(DataModel):
    id = 1
    url = "http://example.com/hook"
    token = "ReplaceMe-ReplaceMe-ReplaceMe-ReplaceMe-"
    push_events = True
    issues_events = False
    confidential_issues_events = False
    merge_requests_events = True
    tag_push_events = True
    note_events = False
    job_events = False
    pipeline_events = False
    wiki_page_events = False
    enable_ssl_verification = True
    #project_id = 0
    #created_at = "2012-10-12T17:04:47Z"