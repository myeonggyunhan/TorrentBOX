#!/bin/bash

if [ $# -ne 2 ]
then
        echo "Usage: $0 <concurrency>"
        exit

nohup python manage.py celeryd -l info -c $1 2>&1 1>../celery.log &

