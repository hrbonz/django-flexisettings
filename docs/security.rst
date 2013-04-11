========
Security
========

Security files
--------------

A very simple way to make sure that passwords are not pushed in your VCS
is to exclude any file matching ``myproject/security*``. It would also
be a good idea to reduce the access to such files by removing read
rights for users other than the one running django.


VCS
---

Files that should not be pushed to your VCS are:

* ``env.py`` : to allow for multiple environments to run at the same
  time. If you're using git, you can add ``myproject/env.py`` in
  ``.gitignore``.
* any security file : repeat after me, **any** security data in your VCS
  is a **bad idea**. If you're using git you can add
  ``myproject/security*.py`` in ``.gitignore``.
