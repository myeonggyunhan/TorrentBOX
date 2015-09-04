#!/bin/bash

if [ $# -ne 1 ]
then
        echo "Usage: $0 <concurrency>"
        exit
fi

nohup python manage.py celeryd -l info -c $1 2>&1 1>celeryLog//celery.log &

