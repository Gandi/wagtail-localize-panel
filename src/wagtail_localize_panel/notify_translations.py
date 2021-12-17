import logging
import textwrap
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from .models import get_users_for_locale, yield_locales

log = logging.getLogger(__name__)


def notify_translators_for_locale(url_prefix, page, locale):
    users = get_users_for_locale(locale)
    users = list(users)
    if not users:
        return

    with translation.override(locale.language_code):
        page_url = url_prefix + reverse(
            "wagtailadmin_pages:edit",
            kwargs={"page_id": page.localized.id},
        )

    status = send_mail(
        f"[CMS][{locale.language_code}] "
        f"New translations required for page {page.title}",
        textwrap.dedent(
            f"""
            Hi,

            The page {page.get_full_url()} has been updated,

            and need to be retranslated in {locale.language_code}.

            New translations are required in {locale.language_code} for the following page:

            * {page.title}: {page_url}

            Regards,
            """
            # TODO add this when we have one
            # Here is a list of all the pages awaiting a translation in {language}:
            # {link to the dashboard when we have one}
        ),
        recipient_list=users,
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False,
    )
    if status == 0:
        raise SMTPException("Unable to send email. Unknown cause.")


def notify_translators(request, page):
    host = request.get_host()
    prefix = f"https://{host}"
    for locale in yield_locales():
        try:
            notify_translators_for_locale(prefix, page, locale)
        except SMTPException:
            log.exception(
                f"Unable to send email notification to '{locale}' translators."
            )
            messages.warning(
                request,
                _(
                    "An error occurred on sending the notification email to "
                    "`%(locale)s` translators. You can retry publishing the page or "
                    "notify manually all translators."
                )
                % {"locale": locale.language_code},
            )
