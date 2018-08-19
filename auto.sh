#!/bin/bash
if [ -e .env ]
then
    . ./.env
else
    echo "Not loading .env - it doesn't exist"
fi
if [ -e venv ] && [ -d venv ]
then
    echo "Virtualenv already installed"
    . venv/bin/activate
else
    echo "Creating new virtualenv"
    virtualenv -p /usr/bin/python3 venv
    . venv/bin/activate
    pip install -r requirements.txt
fi
python3 main.py --gitea  $GITEA_URL\
               --gitlab $GITLAB_URL \
               -r '^BdEINSALyon' \
               --api-key  $API_KEY\
               --personal-token $PERSONAL_TOKEN\
               --fix-mirroring