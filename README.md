# django-flexisettings

Several issues with the standard settings.py are solved in that project :

* get any security configuration (password, secret key, API key, etc) out of the main settings file
* support multiple environments in a flexible way
* automatic discovery and configuration of common project layouts

Qualities of the resulting code :

* generic, don't presume about anything concerning the project
* flexible, allow several configurations to live in the same place and easily switch between them
* simple

# Installation

```shell
$ pip install django-flexisettings
```

# Quickstart

In development, edit `manage.py`, modify the value of `DJANGO_SETTINGS_MODULE` to point at `flexisettings.settings` and add `FLEXI_WRAPPED_MODULE` to point at you project's settings:
```
[...]
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flexisettings.settings")
    os.environ.setdefault("FLEXI_WRAPPED_MODULE", "myproject.settings")
[...]
```

This is all you need to get `flexisettings` to run your settings. At this stage, **nothing** in the configuration object is changed, it is simply wrapped in `flexisettings` proxy object.

Read further for more powerful features of `flexisettings`.

# Configuration

### DJANGO\_SETTINGS\_MODULE

Environment variable to set to point at `flexisettings.settings`

### FLEXI\_WRAPPED\_MODULE

Environment variable to set to point at your django settings, this
environment variable has to be set for `flexisettings` to work.

### FLEXI\_RUN\_ENV

String defining the running environment, used when trying to load
settings depending on the defined running environment.

### FLEXI\_SYS\_PATH

List of paths to add to `sys.path` if they exist, defaults to `['apps',
'lib']`. This will be done if `FLEXI_LAYOUT_DISCOVERY` is `True`.

### FLEXI\_AUTORELOAD

Boolean affecting the autoreload machinery for settings. If set to
`True`, it should make the django autoreload code work when changing any
settings file found in `flexisettings.settings._wrapped_modules`. If set
to `False`, the autoreload will not work on settings. The code is a bit
tricky, not guaranteed to work and might have unsuspected effects, hence
the possibility to disable. Defaults to `True` to preserve django
default behavior.

### FLEXI\_LAYOUT\_DISCOVERY

Boolean that determines if `flexisettings` tries to be smart about your
project layout. It will add any `FLEXI_MEDIA_FOLDER`, `FLEXI_STATIC_FOLDER`,
`FLEXI_TEMPLATE_FOLDERS` folder to the appropriate configuration variables if
they are not already set.

### FLEXI\_MEDIA\_FOLDER

The media folder name to look for when doing layout discovery, defaults to
`'media'`.

### FLEXI\_STATIC\_FOLDER

The static folder name to look for when doing layout discovery, defaults to
`'static'`.

### FLEXI\_TEMPLATE\_FOLDERS

A tuple of template folder names to look for when doing layout discovery,
defaults to `('templates', )`.

### FLEXI\_SITE\_ROOT

Path to the site root, everything that should not be tracked in a VCS
but is still part of your website. For example, the `MEDIA_ROOT` folder
should reside in the site root. This path defaults to
`FLEX_PROJECT_ROOT`.

### FLEXI\_PROJECT\_ROOT

Path to the django project, basically everything that should be tracked
in a VCS. This path defaults to the `dirname()` of the settings folder.


# Example configuration

* edit `env.py` to set the working environment, let's use `prod` here :

```shell
$ cat myproject/env.py
# environment declaration
FLEXI_RUN_ENV = 'prod'
```

* edit `security.py` to set the `SECRET_KEY` value :

```shell
$ grep SECRET_KEY myproject/security.py
SECRET_KEY = 'alongandcomplexsecretstring'
```

* set security variables in `security_prod.py` to be used in any settings file.

```shell
$ grep DEFAULTDB myproject/security_prod.py
DEFAULTDB_NAME = 'dbname'
DEFAULTDB_USER = 'dbuser'
DEFAULTDB_PWD = 'secret'
```

* edit `settings_prod.py` to override generic settings like `DATABASES`, `MEDIA_ROOT`, `TIME_ZONE`

```shell
$ cat myproject/settings/settings_prod.py
[...]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DEFAULTDB_NAME,
        'USER': DEFAULTDB_USER,
        'PASSWORD': DEFAULTDB_PWD,
        'HOST': '',
        'PORT': '',
    }
}
[...]
```

# Layout

```
myproject/__init__.py
          env.py
          security.py
          security_RUN_ENV.py
          settings.py
          settings_RUN_ENV.py
```

* `env.py` has a single variable `FLEXI_RUN_ENV` that defines a running
  environment. This variable is then used to call different profiles of
  configuration depending on the running environment like `dev`, `stage`
  and `prod`. The `FLEXI_RUN_ENV` variable can also be set by
  environment, the environment takes precedence over `env.py`. Example :
```shell
$ export FLEXI_RUN_ENV='dev'; python manage.py runserver
```
* `security.py` holds all the common security variables for the project,
  probably a good place for `SECRET_KEY`.
* `security_RUN_ENV` specific environment security variables, dedicated
  database passwords should go there. Setting defined here will override
  settings defined in `security.py`.
* `settings.py` the classic settings file found in all django projects.
* `settings_RUN_ENV.py` gathers local settings for a given running
  environment, settings defined here will override settings defined in
  `settings.py`.

# Loading order

The modules are loaded in the following order :

1. `myproject/env.py`
2. `myproject/security.py`
3. `myproject/security_RUN_ENV.py`
4. `myproject/settings.py`
5. `myproject/settings_RUN_ENV.py`

# Security files

A very simple way to make sure that passwords are not pushed in your VCS
is to exclude any file matching `myproject/security*`. It would also be
a good idea to reduce the access to such files by removing read rights
for users other than the one running django.

# Miscellaneous

If the `FLEXI_RUN_ENV` variable is false in python, the only settings files read are `security.py` and `settings.py`.

Modifying the settings does not reload the server when using `manage.py runserver`.

Files that should not be pushed to your VCS are :

* `env.py` : to allow for multiple environments to run at the same time
* and avoid problems with git pulls. For this you can add `myproject/env.py` in `.gitignore`.
* any security file : repeat after me, any security data in your VCS is
* a **bad idea**. For this you can add `myproject/security*.py` in `.gitignore`.

# Debugging

To help in the debugging process, it is possible to know which files have been included in the final settings object by accessing `flexisettings.settings._wrapped_modules`. An example from the unit tests, the project name is 'testProject' and the running environment is 't':

```
$ python manage.py shell
[...]
>>> import flexisettings.settings
>>> flexisettings.settings._wrapped_modules
{'testProject.env': '/path/to/django-flexisettings/t/testProject/env.py',
 'testProject.security': '/path/to/django-flexisettings/t/testProject/security.py',
 'testProject.settings': '/path/to/django-flexisettings/t/testProject/settings.py',
 'testProject.settings_t': '/path/to/django-flexisettings/t/testProject/settings_t.py'}
```

# References

* [Django project](https://www.djangoproject.com/)
* [Django settings](https://docs.djangoproject.com/en/dev/topics/settings/)
* [Splitting up the settings file](https://code.djangoproject.com/wiki/SplitSettings)

## Project layouts

* [Django Project Conventions, Revisited](http://zacharyvoase.com/2010/02/03/django-project-conventions/) (Zachary Voase)
* [django-resusable-app](http://django-reusable-app-docs.readthedocs.org/en/latest/index.html)
* [pinax-project-zero](https://github.com/pinax/pinax-project-zero)
* [Django Project Structure](http://www.deploydjango.com/django_project_structure/)
* [A general django project structure or folder layout](http://timmyomahony.com/blog/2012/11/09/general-django-project-structure-or-folder-layout/)

# License

django-flexisettings is published under a 3-clause BSD license, see LICENSE.
