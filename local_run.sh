#!./bin/sh


# # Using virtualenv and requirement.txt file
# if [ -d ".flash_card_env" ];
# # if [ -d ".venv" ];
# then
#     echo "Enabling venv"
# else
#     echo "Create venv"
#     exit N
# fi

# source .flash_card_env/bin/activate
# # source .venv/bin/activate
# export ENV=development
# python main.py
# deactivate

# Using pipenv and pipfile
pipenv run python main.py
exit
