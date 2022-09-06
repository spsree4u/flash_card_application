#!./bin/sh

# # Using virtualenv and requirement.txt file
# virtualenv -p python3 .flash_card_env
# if [ -d ".flash_card_env" ];
# # if [ -d ".venv" ];
# then
#     echo "Enabling venv"
#     source .flash_card_env/bin/activate
#     pip install -r requirements.txt
#     deactivate
# else
#     echo "Create venv"
#     exit N
# fi

# Using pipenv and pipfile
pip install pipenv
pipenv install --ignore-pipfile
pipenv --venv
pipenv check
