#!/bin/bash
. ./.env
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
python3 main.py --gitea 'https://git.ribes.me' \
               --gitlab 'https://git.bde-insa-lyon.fr' \
               -r '^BdEINSALyon' \
               --api-key  $API_KEY\
               --personal-token $PERSONAL_TOKEN\
               --fix-mirroring