#!/bin/bash

# System params
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Dump db
source ${DIR}/venv/bin/activate
echo -e "\033[92m\nMake db dump... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py dumpdata users preferences telegram survey profi --exclude survey.import --exclude survey.tasksexecution --exclude survey.tasksexecutionimage --indent 4 > ${DIR}/data/initial.json
deactivate

# Dump media
cd ${DIR}
tar -pczf ${DIR}/data/media.tar.gz --exclude ./media/tasks/exec/* ./media --totals

# End
echo -e ""
