# sync-bde

Script python qui permet un mirroring automatique des repos GitLab vers mon Gitea
Utilise **Python v3.5+**
# Utilisation
Créez un utilisateur sur le serveur Gitea qui recevra les backups et créez un nouveau Access Token
(*Settings*>*Applications*>*Generate new Token*)
Spécifiez une regex qui sera utilisée pour choisir si le repo doit être sauvegardé.

Aide :
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
# Gitea
Les projets migrés sur Gitea verront leur nom modifié, car les dossiers (*namespaces*)
n'existent pas sur Gitea. Vu qu'ils existent sur Gitlab,
on aurait des cas où deux repo différents sur GitLab (`adhesion/api` et `billevent/api`)
se retrouveraient avec le même nom sur Gitea. Super comme sauvegarde ...

Du coup les `/` sont transformés en `_._`

Exemple :
`billevent/ticket-reader` devient `billevent_._ticket-reader`

# Fonctionnement attendu
Ce script devra faire en sorte de créer des miroir de tous les projets Gitlab vers un Gitea.
Il pourra aussi activer la mise à jour automatique de Gitea.
Idéalement il devrait vérifier quels repos sont manquants sur Gitea et alerter si des
projets ont leur auto-miroir désactivé

## Bugs & fonctionnalités manquantes
Il n'est pas possible de sauvegarder un repo privé
la regex ne marche pas tout le temps (``^BdE` matche `al26p/home-lock_reader`