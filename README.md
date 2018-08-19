mirror-gitlab-gitea
===================

[![](https://img.shields.io/docker/pulls/jeanribes/mirror-gitlab-gitea.svg)](https://hub.docker.com/r/jeanribes/mirror-gitlab-gitea/)

![](https://badgen.net/badge/Python/3.5+/green)  ![](https://badgen.net/badge/License/GPLv3/cyan)

This software aims at helping unstable [Gitlab](https://gitlab.com) deployments (badly dockerized !) by setting up mirrors to a simpler Git web host, [Gitea server](https://gitea.io/).

It consits of a Python script that mirror all regex-matching Gitlab projects on a Gitea server in bulk.
Can be run as a dameon to start mirror any new project.

# Setup
## Requirements
* Python 3.5+
* virtualenv
You will need
* a dedicated account on a [Gitea server](https://gitea.io/) along with a corresponding **API Key**, that can be generated in *Settings*>*Applications*>*Generate new Token*
* a gitlab **Personal Access Token** for mirroring private repositories (required), get it in *Settings > Access Tokens*
## Docker daemon
```
$ docker pull jeanribes/mirror-gitlab-gitea
$ docker run -d -e API_KEY='' -e PERSONAL_TOKEN='' -e GITEA_URL='' -e GITLAB_URL='' -e REPO_REGEX='' -e TIME_INTERVAL=24h jeanribes/mirror-gitlab-gitea
```
## Docker one-off command
```
$ docker run -rm jeanribes/mirror-gitlab-gitea python main.py -h
```
## Shell
```
$ git clone https://github.com/JeanRibes/mirror-gitlab-gitea.git && cd mirror-gitlab-gitea
$ ./auto.sh -h #will install a virtualenv on the first run
```
The helper script `auto.sh` will attempt to load required values from a `.env` file when given no argument
```
API_KEY= #gitea api key
PERSONAL_TOKEN=#gitlab personal token
GITEA_URL=
GITLAB_URL=
REPO_REGEX= #regex that specifies which repos will be synced by matching the full path
```
### Options
* **-r**, *REPO_REGEX* : only the Gitlab projects that match this regex will be mirrored.
* **--fix-missing** : All Gitea repos owned by the mirroring user that have their mirroring status disabled will be deleted and re-created.
This is the default when you are not typing command-line switches by yourself.

# Tips
Don't use your personal Gitea account with dæmonized scripts.

Or if you do so, be warned that an incorrecly configured script may fill up your dashboard with mirrored repositories.
If you use the `auto.sh` script without arguments or the Docker dæmon, it may wipe your repos and replace them with mirrored gitlab projects !

I am not responsible for wiped repos !

Note that Gitea pulls new commits every 8 hours when mirroring mode is activated (always with this script).
You only need to run this script when you create new projects that are not yet being automatically mirrored
## Gotchas
As mirrored projects will be migrated as **mirrors**, you can't push to them. Instead of converting the Gitea repo to a non-mirror one (it may get deleted depending on your setup), you should **fork** them.

It may be best to commit into a new branch, so that when Gitlab is back again you don't have to merge in the event that someone worked offline and waited for Gitlab to be operationnal again.
## Issues
This version of the script will download a list of **all** the reachable repositories through the GitLab API (pagination enabled).
It may not be a good idea to run it against [Gitlab.com](https://gitlab.com)

# Contributing
I will be happy to accept any relevant contribution, as long as the current features are working !

## Possible improvements
* Mirroring from GitLab to Github
* from GitHub to Gitea.
* Side-kicking a script that manually mirrors to SSH hosts, or uncompatible Git Web hosts

# Instructions Françaises

Script python qui permet un mirroring automatique des repos GitLab vers mon Gitea

Le conteneur Docker va exécuter le script toutes les x heures pour récupérer les nouveaux repos.
Pendant ce temps-là, Gitea va pull les repos toutes les 8 heures.

Utilise **Python v3.5+**

## Installation
### Avec Docker
```
docker build -t image_name .
docker run -d -e API_KEY= -e PERSONAL_TOKEN= -e GITEA_URL= -e GITLAB_URL= -e REPO_REGEX="" -e TIME_INTERVAL=24h image_name #va tourner continuellement
#ou en utilisant la ligne de commande directement, 'one-off'
docker run --rm image_name python main.py -h
```

### Locale
`sh auto.sh`
Le script automatique prend ses valeurs depuis `.env`
```
API_KEY= #gitea api key
PERSONAL_TOKEN=#gitlab personal token
GITEA_URL=
GITLAB_URL=
REPO_REGEX= #regex that specifies which repos will be synced by matching the full path
```
Pour cloner tous les repos du BdE, on peut utiliser la regex `"^BdEINSALyon"` par exemple

## Utilisation
### Pré-requis
Créez un utilisateur sur le serveur Gitea qui recevra les backups et créez un nouveau Access Token.
(*Settings*>*Applications*>*Generate new Token*)
Spécifiez une regex qui sera utilisée pour choisir si le repo doit être sauvegardé.
### Restauration
Pour travailler quand Gitlab est down (souvent xD lol), il suffit de se créer un compte sur Gitea et de forker les repos sauvegardés.
Ne désactivez pas le mirroring pour commit sur un repo Gitea, sinon il sera supprimmé et re-crée depuis Gitlab !
## Aide
```
usage: main.py [-h] [--personal-token [token]] [--api-key token] [--gitlab url] [--gitea url] [-c [file]] [-r [regex]] [-S]

Set up automatic mirroring from GitLab to Gitea in batch

optional arguments:
  -h, --help            show this help message and exit
  --personal-token [token]
                        Your Gitlab personal access token. Will be sent to gitea host to clone private repos
  --api-key token       Your Gitea api key. Needed to migrate repos
  --gitlab url          URL of the Gitlab host
  --gitea url           URL of the Gitea host
  -c [file]             Configuration file
  -r [regex]            The full path of repositories will need to match this regex
  -S                    Save command-line arguments to config file

While the Gitlab token is optionnal, the script will fail if the repositories are private
```
## Gitea
Les projets migrés sur Gitea verront leur nom modifié, car les dossiers (*namespaces*)
n'existent pas sur Gitea. Vu qu'ils existent sur Gitlab,
on aurait des cas où deux repo différents sur GitLab (`adhesion/api` et `billevent/api`)
se retrouveraient avec le même nom sur Gitea. Super comme sauvegarde ...

Du coup les `/` sont transformés en `_._`

Exemple :
`billevent/ticket-reader` devient `billevent_._ticket-reader`

## Fonctionnement attendu
Ce script devra faire en sorte de créer des miroir de tous les projets Gitlab vers un Gitea.
Il devra aussi activer la mise à jour automatique de Gitea.
Idéalement il devrait vérifier quels repos sont manquants sur Gitea et alerter si des
projets ont leur auto-miroir désactivé

## Bugs & fonctionnalités manquantes
la regex ne marche pas tout le temps (``^BdE` matche `al26p/home-lock_reader`)