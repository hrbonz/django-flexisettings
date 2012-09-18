# django-flexisettings

Several issues with the standard settings.py are solved in that project :

* get any security configuration (password, secret key, API key, etc) out of the main settings file
* support multiple environments in a flexible way

Qualities of the resulting code :

* generic, don't presume about anything concerning the project
* flexible, allow several configurations to live in the same place and easily switch between them
* simple

# References

* [Django project](https://www.djangoproject.com/)
* [Django settings](https://docs.djangoproject.com/en/dev/topics/settings/)
* [Splitting up the settings file](https://code.djangoproject.com/wiki/SplitSettings)

# License

See LICENSE
