#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURR_DIR="${DIR##*/}"
PROJECT_NAME=${CURR_DIR//[-.]/_}

export DJANGO_SETTINGS_MODULE='application.settings'

source ${DIR}/venv/bin/activate
cd ${DIR}/src
celery -A application inspect active
deactivate
