#!/bin/sh
if [ -e .env ] 
then
    . ./.env
else
        if [ $# == 0 ]
	then
		echo "Not loading .env - it doesn't exist"
	fi
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
#if [ "$#" != "0" ]
if [ $# != 0 ]
then
	python3 main.py $@
else
	python3 main.py --gitea  $GITEA_URL\
               --gitlab $GITLAB_URL \
               -r $REPO_REGEX \
               --api-key  $API_KEY\
               --personal-token $PERSONAL_TOKEN\
               --fix-mirroring
fi