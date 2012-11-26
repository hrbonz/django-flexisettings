# django-flexisettings

Several issues with the standard settings.py are solved in that project :

* get any security configuration (password, secret key, API key, etc) out of the main settings file
* support multiple environments in a flexible way

Qualities of the resulting code :

* generic, don't presume about anything concerning the project
* flexible, allow several configurations to live in the same place and easily switch between them
* simple

# Installation

* Get the source code :

```shell
$ git clone https://github.com/hrbonz/django-flexisettings.git
```

* copy the `settings/` folder to your project folder (where `settings.py`
  should be) :

```shell
$ cp -r django-flexisetttings/settings /path/to/django/myproject/
```

* copy `myproject/settings.py` in the `myproject/settings/` folder

# Layout

```
myproject/settings/__init__.py
                   env.py
                   security.py
                   security_RUN_ENV.py
                   settings.py
                   settings_RUN_ENV.py
```

* `__init__.py` contains all the black magic, **HERE BE DRAGONS AND
  UNICORNS**.
* `env.py` has a single variable `RUN_ENV` that defines a running
  environment. This variable is then used to call different profiles of
  configuration depending on the running environment like `dev`, `stage`
  and `prod`. The `RUN_ENV` variable can also be set by environment, the environment takes precedence over `env.py`. Example :
```shell
$ export RUN_ENV='dev'; python manage.py runserver
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

1. `settings`
2. `settings/env.py`
3. `settings/security.py`
4. `settings/security_RUN_ENV.py`
5. `settings/settings.py`
6. `settings/settings_RUN_ENV.py`

# Security files

A very simple way to make sure that passwords are not pushed in your VCS is to exclude any file matching `myproject/settings/security*`. It would also be a good idea to reduce the access to such files by removing read rights for users other than the one running django.

# Miscellaneous

Modifying the settings does not reload the server when using `manage.py runserver`. To do so, simply use the command `touch(1)` on `settings/__init__.py` or restart the server.

# References

* [Django project](https://www.djangoproject.com/)
* [Django settings](https://docs.djangoproject.com/en/dev/topics/settings/)
* [Splitting up the settings file](https://code.djangoproject.com/wiki/SplitSettings)

# License

See [LICENSE](LICENSE)
