import logging

from django.template.loader import render_to_string

from .models import get_missing_translations_stat

log = logging.getLogger(__name__)


class WorkflowPagesToTranslatePanel:
    name = "workflow_pages_to_translate"
    order = 100

    def __init__(self, request, locale):
        self.request = request
        self.locale = locale
        self.pages = get_missing_translations_stat(locale)

    def render(self):
        log.info("Rendering the translation workflow")
        pages = list(self.pages)
        return render_to_string(
            "wagtail_localize_panel/home/workflow_pages_to_translate.html",
            {"pages": pages, "locale": self.locale},
            request=self.request,
        )
