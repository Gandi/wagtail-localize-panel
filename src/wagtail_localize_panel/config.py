"""Load settings for the wagtail-oauth2 app."""
from django.conf import settings

global_prefix = "LOCALIZE_PANEL_"


def get_setting(name, default=None):
    """Get the settings without the prefix."""
    return getattr(settings, global_prefix + name, default)


def get_app_label():
    app_label = get_setting("APP_NAME")
    if app_label is None:
        raise RuntimeError("Missing key LOCALIZE_PANEL_APP_NAME")
    return app_label