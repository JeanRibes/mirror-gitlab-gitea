# sync-bde

Script python qui permet un mirroring automatique des repos GitLab vers mon Gitea

# Gitea
Les projets migrés sur Gitea verront leur nom modifié, car les dossiers (*namespaces*)
n'existent pas sur Gitea. Vu qu'ils existent sur Gitlab,
on aurait des cas où deux repo différents sur GitLab (`adhesion/api` et `billevent/api`)
se retrouveraient avec le même nom sur Gitea. Super comme sauvegarde ...

Du coup les '/' sont transformés en '_._'

Exemple :
`billevent/ticket-reader` devient `billevent_._ticket-reader`

# Fonctionnement attendu
Ce script devra faire en sorte de créer des miroir de tous les projets Gitlab vers un Gitea.
Il pourra aussi activer la mise à jour automatique de Gitea.
Idéalement il devrait vérifier quels repos sont manquants sur Gitea et alerter si des
projets ont leur auto-miroir désactivé