FROM ubuntu:14.04
MAINTAINER gotlium <gotlium@gmail.com>

RUN apt-get update && apt-get install -y git \
    python python-dev python-pip && \
    apt-get clean

ADD ./demo/ /mmc_demo

RUN pip install -r /mmc_demo/requirements.txt

RUN python /mmc_demo/manage.py syncdb --noinput
RUN python /mmc_demo/manage.py migrate --noinput
RUN python /mmc_demo/manage.py loaddata /mmc_demo/auth.json

RUN /bin/bash -c 'python /mmc_demo/manage.py test_command >& /dev/null'
RUN /bin/bash -c 'python /mmc_demo/manage.py test_command_noargs >& /dev/null'
RUN /bin/bash -c 'python /mmc_demo/manage.py test_command_error >& /dev/null || true'
RUN /bin/bash -c 'python /mmc_demo/manage.py test_command_killed >& /dev/null || true'

CMD /bin/bash -c 'python /mmc_demo/manage.py runserver 0.0.0.0:8000'

EXPOSE 8000
