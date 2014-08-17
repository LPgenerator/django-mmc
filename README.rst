Django-mmc
==========

.. image:: https://api.travis-ci.org/LPgenerator/django-mmc.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/LPgenerator/django-mmc
.. image:: https://coveralls.io/repos/LPgenerator/django-mmc/badge.png?branch=master
    :target: https://coveralls.io/r/LPgenerator/django-mmc?branch=master
.. image:: https://pypip.in/v/django-mmc/badge.png
    :alt: Current version on PyPi
    :target: https://crate.io/packages/django-mmc/
.. image:: https://pypip.in/d/django-mmc/badge.png
    :alt: Downloads from PyPi
    :target: https://crate.io/packages/django-mmc/


What's that
-----------
App for monitoring management commands on Django.


Quick installation
------------------
1. Using pip:

.. code-block:: bash

    $  pip install django-mmc


2. Add ``mmc`` application to ``INSTALLED_APPS`` in your settings file

3. Inject management classes before apps will be loaded

.. code-block:: python

    from mmc.mixins import inject_management

    inject_management()


4. Sync database (``./manage.py syncdb`` or ``./manage.py migrate``)

5. Enjoy


Local demo installation
-----------------------

.. code-block:: bash

    $ sudo apt-get install virtualenvwrapper
    $ mkvirtualenv django-mmc
    $ git clone https://github.com/LPgenerator/django-mmc.git
    $ cd django-mmc
    $ python setup.py develop
    $ cd demo
    $ pip install -r ../requirements/dev.txt
    $ python manage.py syncdb
    $ python manage.py test_command >& /dev/null
    $ python manage.py test_command_noargs >& /dev/null
    $ python manage.py test_command_error >& /dev/null
    $ python manage.py runserver >& /dev/null &
    $ xdg-open http://127.0.0.1:8000/admin/mmc/mmclog/


Configuration
-------------

1. Execute the command, and script will be available at http://127.0.0.1:8000/admin/mmc/mmcscript/
2. Configure script options on script settings http://127.0.0.1:8000/admin/mmc/mmcscript/1/
3. Add email addresses for errors notification http://127.0.0.1:8000/admin/mmc/mmcemail/
4. All logs available on Logs page http://127.0.0.1:8000/admin/mmc/mmclog/
5. If you are using sentry, configure sentry, and all errors will be send into sentry too


Usage without inject
--------------------

If you want track only specified commands manually without auto-inject,
follow to examples below:

.. code-block:: python

    # args
    from mmc.mixins import BaseCommand


    class Command(BaseCommand):
        def handle(self, *args, **options):
            print "OK"


    # noargs
    from mmc.mixins import NoArgsCommand


    class Command(NoArgsCommand):
        def handle_noargs(self, *args, **options):
            print "OK"


When you are using auto-inject, you can use ignore flag on Scripts/Hosts settings.
Logs about execution not be stored, but if you got any error on your commands,
you will be notified to emails.


Screenshots
-----------
.. image:: /screenshots/log_changelist.jpg
.. image:: /screenshots/script_changelist.jpg
.. image:: /screenshots/email_changelist.jpg
.. image:: /screenshots/hosts_changelist.jpg


Compatibility:
-------------
* Python: 2.6, 2.7
* Django: 1.3.x, 1.4.x, 1.5.x, 1.6.x, 1.7.x
