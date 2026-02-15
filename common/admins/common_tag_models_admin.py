from django.contrib import admin

from common.models.common_tag_models import Tag

from common.admins.base import _HatchUpBaseAdmin, admin_site


@admin.register(Tag, site=admin_site)
class TagAdmin(_HatchUpBaseAdmin):
    list_display = ("id", "type", "name", "slug", "created_at", "is_active")
    list_filter = _HatchUpBaseAdmin.list_filter + ("type",)
    search_fields = ("name", "slug")
    date_hierarchy = "created_at"
