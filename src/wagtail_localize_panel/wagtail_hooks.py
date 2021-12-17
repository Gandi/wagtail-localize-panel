from django.contrib.auth.models import Permission
from wagtail.core import hooks
from wagtail.core.models import Locale

from .config import get_app_label
from .models import get_locale_for_user
from .notify_translations import notify_translators
from .utils import update_translations
from .views import WorkflowPagesToTranslatePanel



@hooks.register("register_permissions")
def register_localize_panel():
    return Permission.objects.filter(
        content_type__app_label="wagtail_localize_panel", codename="view_localize_panel"
    )


@hooks.register("register_permissions")
def register_submit_translation_permission():
    return Permission.objects.filter(
        content_type__app_label="wagtail_localize_panel", codename="optin_translation"
    )


@hooks.register("after_publish_page")
def register_admin_urls(request, page):
    locale = Locale.objects.filter(language_code="en").first()

    if page.locale_id == locale.id:
        update_translations(page)
        notify_translators(request, page)


@hooks.register("construct_homepage_panels")
def register_page_to_translate(request, panels):
    for locale in get_locale_for_user(request):
        panels.append(WorkflowPagesToTranslatePanel(request, locale))
