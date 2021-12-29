Install and configure wagtail-localize-panel
============================================


Installation
------------

``wagtail-localize-panel`` is available on pypi, you can install with your favorite
packaging tool.

.. note::

   Example using pip

   ::

      pip install wagtail-localize-panel

Django's Configuration
----------------------

INSTALLED_APPS
~~~~~~~~~~~~~~

``wagtail-localize-panel`` is a Django application that must be installed,
so it must be in the ``INSTALLED_APPS`` list of your settings module.
And, to work, it requires other app that are probably already installed.

Here is the lists of the minimum installed app.

::

   INSTALLED_APPS = [
      # ...
      "django.contrib.auth",
      "django.contrib.contenttypes",
      "django.contrib.sessions",
      "wagtail_oauth2",
      "wagtail.admin",
      "wagtail.users",
      "wagtail.core",
      "wagtail_localize",
      "wagtail.locales",
      "wagtail_localize_panel",
      # ...
   ]


TEMPLATES
~~~~~~~~~

`wagtail-localize-panel` render an admin template `workflow_pages_to_translate.html`
for the translators.

The template is provided using django template system in the package,
the settings `APP_DIRS` must be set to `True` in order to render it.

::

   TEMPLATES = [
      {
         "BACKEND": "django.template.backends.django.DjangoTemplates",
         "APP_DIRS": True,
      }
   ]


SETTINGS
~~~~~~~~

The wagtail site appname that needs to be translated must be passed
in parameter in a parameter ``LOCALIZE_PANEL_APP_NAME``.

::

   LOCALIZE_PANEL_APP_NAME = "<appname>"


Wagtail email must also be properly set, for example:


::

   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_HOST = "smtp.example.net"
   EMAIL_PORT = 25
   WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = "wagtail-admin-email@example.net"



.. note::

   If the django user model has been redefined, e.g. not ``auth_``,
   then the prefix must be set using the setting ``LOCALIZE_PANEL_AUTH_PREFIX``

   ::

      LOCALIZE_PANEL_AUTH_PREFIX = "<prefix>_"

