==============================
Installation and configuration
==============================

.. include install section from README file
.. include:: ../README.rst
   :start-line: 14
   :end-line: 22


Configuration
-------------

.. include development configuration from README file
.. include:: ../README.rst
   :start-line: 27
   :end-line: 57

Gunicorn
^^^^^^^^

Following `django's recommandations
<https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/gunicorn/>`_ on
how to use gunicorn, the project will run in WSGI mode.

First edit the ``myproject/wsgi.py`` file as shown in the :ref:`wsgi-app-conf`
paragraph.

Command line
""""""""""""

::

    $ cd /path/to/myproject
    $ /path/to/venv/bin/python gunicorn --workers=42 myproject.wsgi:application


Debian
""""""

The configuration file for gunicorn should be saved as
``/etc/gunicorn.d/myproject`` and contain::

    CONFIG = {
        'python': '/path/to/venv/bin/python',
        'working_dir': '/path/to/myproject',
        'user': 'www-data',
        'group': 'www-data',
        'args': (
            'myproject.wsgi:application',
        ),
    }

Extra options that could be useful in the ``args`` tuple:
    * ``'--bind=ip:port'``: set which ip and port the process whould bind to
    * ``'--workers=#'``: set the number of workers to spawn

For more information on gunicorn configuration, `read the docs
<http://docs.gunicorn.org/en/latest/configure.html>`_.
