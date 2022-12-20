#!/bin/bash

result=`flake8 "/code/src/application/users/views.py"`

echo $result > /code/src/application/users/result_flake8.txt
echo $result
