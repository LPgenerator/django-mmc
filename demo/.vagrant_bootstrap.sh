#!/bin/bash

apt-get update
apt-get install -y git python python-dev python-pip
apt-get clean

cd /mmc_demo/
pip install -r requirements.txt

if [ -f "db.sqlite" ]; then rm ./db.sqlite; fi

python manage.py syncdb --noinput
# python manage.py migrate --noinput
python manage.py loaddata auth.json

python manage.py test_command >& /dev/null &
python manage.py test_command_noargs >& /dev/null &
python manage.py test_command_error >& /dev/null &
python manage.py test_command_killed >& /dev/null &

nohup python manage.py runserver 0.0.0.0:8000 >& /dev/null &
