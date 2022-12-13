#!/bin/bash

# System params
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURR_DIR="${DIR##*/}"
PROJECT_NAME=${CURR_DIR//[-.]/_}

export DJANGO_SETTINGS_MODULE='application.settings'

# Pulling
source ${DIR}/venv/bin/activate

echo -e "\033[92m\nGit pull... Press enter to continue...\033[0m" & read
git pull

echo -e "\033[92m\nSync database... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py migrate
echo -e " "
python ${DIR}/src/manage.py syncprefs

echo -e "\033[92m\nSync static files... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py collectstatic

#echo -e "\033[92m\nStop celery\033[0m" & read
#cd ${DIR}/src
#celery -A application control shutdown

echo -e "\033[92m\nRestart supervisor... Press enter to continue...\033[0m" & read
supervisorctl restart $CURR_DIR
if [ "$1" == "celery" ]; then
  supervisorctl restart ${CURR_DIR}_celery
fi

deactivate
