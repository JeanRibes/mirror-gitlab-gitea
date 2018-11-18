#!/bin/sh
while true
do
    echo "Launching script"
    set -x
    python3 main.py --gitea  $GITEA_URL\
               --gitlab $GITLAB_URL \
               -r $REPO_REGEX \
               --api-key  $API_KEY\
               --personal-token $PERSONAL_TOKEN\
               --fix-mirroring
    sleep $TIME_INTERVAL
done