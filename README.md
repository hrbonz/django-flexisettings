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
$ git clone https://github.com/stefan-berder/django-flexisettings.git
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
                   local_settings_RUN_ENV.py
                   security.py
                   security_RUN_ENV.py
                   settings.py
```

* `__init__.py` contains all the black magic, **HERE BE DRAGONS AND
  UNICORNS**.
* `env.py` has a single variable `RUN_ENV` that defines a running
  environment. This variable is then used to call different profiles of
  configuration depending on the running environment like `dev`, `stage`
  and `prod`.
* `local_settings_RUN_ENV.py` gathers local settings for a given running
  environment, settings defined here will override settings defined in
  `settings.py`.
* `security.py` holds all the common security variables for the project,
  probably a good place for `SECRET_KEY`.
* `security_RUN_ENV` specific environment security variables, dedicated
  database passwords should go there. Setting defined here will override
  settings defined in `security.py`.
* `settings.py` the classic settings file found in all django projects.

# Loading order

The modules are loaded in the following order :

1. `settings`
2. `settings.env`
3. `settings.security`
4. `settings.security_RUN_ENV`
5. `settings.settings`
6. `settings.local_settings_RUN_ENV`

# References

* [Django project](https://www.djangoproject.com/)
* [Django settings](https://docs.djangoproject.com/en/dev/topics/settings/)
* [Splitting up the settings file](https://code.djangoproject.com/wiki/SplitSettings)

# License

See LICENSE
