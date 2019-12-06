#!/bin/sh
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0"]]; then
        break
    fi
    echo Db Upgrade failed, retrying in 5 seconds...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - krunchly:app