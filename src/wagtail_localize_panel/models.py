from collections import namedtuple

from django.contrib.auth import get_user
from django.db import connection
from django.urls import reverse
from django.utils import translation
from wagtail.core.models import Locale

from .config import get_app_label, get_user_table, get_users_group_table


PageToTranslate = namedtuple(
    "PageToTranslate",
    [
        "slug",
        "title",
        "localized_url",
        "source_cnt",
        "trans_cnt",
        "trans_prc",
    ],
)


def yield_locales():
    locales = Locale.objects.all()
    for locale in locales:
        if locale.language_code == "en":
            continue
        yield locale


def get_locale_for_user(request):
    user = get_user(request)
    appname = get_app_label()
    user_groups_table = get_users_group_table()
    if appname is None:
        raise RuntimeError("Missing key LOCALIZE_PANEL_APP_NAME")
    query = f"""
    select wagtailcore_locale.id, wagtailcore_locale.language_code
    from wagtailcore_locale
    inner join wagtailcore_page on wagtailcore_locale.id = wagtailcore_page.locale_id
    inner join wagtailcore_grouppagepermission gperm on gperm.page_id = wagtailcore_page.id
        and gperm.permission_type = 'edit'
    inner join django_content_type ctype on ctype.app_label = 'wagtail_localize_panel'
        and ctype.model = 'localize_panel'
    inner join auth_permission on auth_permission.content_type_id = ctype.id
                and auth_permission.codename = 'view_localize_panel'
    inner join auth_group_permissions on auth_group_permissions.permission_id = auth_permission.id
    inner join auth_group on auth_group.id = auth_group_permissions.group_id and
        gperm.group_id = auth_group.id
    inner join {user_groups_table} on {user_groups_table}.group_id = auth_group.id
        and  {user_groups_table}.user_id = {user.id};
    """
    locales = Locale.objects.raw(query)
    return locales


def get_users_for_locale(locale):
    """Get the list of user for the given local."""
    users = get_user_table()
    user_groups = get_users_group_table()
    query = f"""
    select {users}.first_name, {users}.last_name, {users}.email
    from {users}
    inner join {user_groups} on {user_groups}.user_id = {users}.id
    inner join auth_group on {user_groups}.group_id = auth_group.id
    inner join auth_group_permissions on auth_group.id = auth_group_permissions.group_id
    inner join auth_permission on permission_id = auth_permission.id and codename = 'optin_translation'
    inner join django_content_type on auth_permission.content_type_id = django_content_type.id
            and app_label = %s and model = 'optin_translation'
    inner join wagtailcore_grouppagepermission on wagtailcore_grouppagepermission.group_id = auth_group.id
        and wagtailcore_grouppagepermission.permission_type = 'edit'
    inner join wagtailcore_page on wagtailcore_grouppagepermission.page_id = wagtailcore_page.id
         and wagtailcore_page.locale_id = %s
    """

    cursor = connection.cursor()
    appname = get_app_label()
    cursor.execute(
        query,
        (
            appname,
            locale.id,
        ),
    )
    for row in cursor.fetchall():
        name = f"{row[0]} {row[1]}".strip() or row[2]
        yield f"{name} <{row[2]}>"


def get_missing_translations_stat(locale):
    query = """
    select stat.slug, trans.id as trans_id, stat.title, stat.source_cnt, stat.trans_cnt, (stat.trans_cnt * 100 / stat.source_cnt::float) as prc
    from (
        select slug, title, translation_key, count(source) as source_cnt, count(trans) as trans_cnt
        from (
            select p.slug, p.translation_key, p.title, s.data as source, st.data as trans
            from wagtailcore_page p
            inner join wagtail_localize_translationsource ts on ts.object_id = p.translation_key
            inner join wagtail_localize_stringsegment ss on ss.source_id = ts.id
            inner join wagtail_localize_string s on ss.string_id = s.id and s.locale_id = 1
            left join wagtail_localize_stringtranslation st on st.translation_of_id = s.id
                 and ss.context_id = st.context_id
                 and st.locale_id = %s
            where p.locale_id = 1
        ) as t
        group by 1, 2, 3
        having count(source) != count(trans)
    ) stat
    inner join wagtailcore_page trans on stat.translation_key = trans.translation_key and trans.locale_id = %s
    order by prc, trans_cnt, source_cnt;
    """
    cursor = connection.cursor()
    cursor.execute(
        query,
        (
            locale.id,
            locale.id,
        ),
    )
    with translation.override(locale.language_code):
        for row in cursor.fetchall():
            page_url = reverse(
                "wagtailadmin_pages:edit",
                kwargs={"page_id": row[1]},
            )
            # Row 0 should be the get_admin_display url
            # but it will makes one query per page here...
            yield PageToTranslate(row[0], row[2], page_url, row[3], row[4], row[5])
