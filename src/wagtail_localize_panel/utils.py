from wagtail_localize.models import TranslationSource


def update_translations(page):
    trans_source, created = TranslationSource.get_or_create_from_instance(page)
    if not created:
        trans_source.update_from_db()
