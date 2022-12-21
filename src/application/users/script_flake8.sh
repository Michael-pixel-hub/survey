#!/bin/bash

echo -n > /code/src/application/users/result_flake8.txt

flake8 "/code/src/application/users/views.py" | tee /code/src/application/users/result_flake8.txt

VAR1=`cat /code/src/application/users/result_flake8.txt`

if [[ -z $VAR1 ]]
  then
    echo 'The check is completed. No errors detected'
fi