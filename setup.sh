#!/bin/bash
source venv/bin/activate
DATABASE=$(sed 's/\.*+.*//' <<< $DATABASE_URL)
if [ "$DATABASE" = "mysql" ]
then
        DATABASE_HOST=$(sed 's/.*@\(.*\):.*/\1/' <<< $DATABASE_URL)
        DATABASE_PORT=$(sed 's/.*:\(.*\)\/.*/\1/' <<< $DATABASE_URL)
        until nc -w 5 -z $DATABASE_HOST $DATABASE_PORT
        do
                echo "Waiting for database..."
                sleep 5
        done
    echo "Database started"
fi
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - krunchly:app