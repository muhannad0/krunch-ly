#!/bin/sh
source venv/bin/activate
if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for database..."
    echo "Db started"
fi
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - krunchly:app