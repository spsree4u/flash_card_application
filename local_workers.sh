#!./bin/sh

# if [ -d ".flash_card_env" ];
# then
#     echo "Enabling venv"
# else
#     echo "Create venv"
#     exit N
# fi

# source .flash_card_env/bin/activate
# export ENV=development
# celery -A main.celery worker -l info
# deactivate

pipenv run celery -A main.celery worker -l info
exit
