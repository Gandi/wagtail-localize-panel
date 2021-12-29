"""Load settings for the wagtail-localize-panel app."""
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


def get_auth_prefix():
    return get_setting("AUTH_PREFIX", "auth")


def get_users_group_table():
    return f"{get_auth_prefix()}_user_groups"


def get_user_table():
    return f"{get_auth_prefix()}_user"