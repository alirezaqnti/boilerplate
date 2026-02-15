from django.contrib import admin

from common.models.common_industry_models import Industry

from common.admins.base import _HatchUpBaseAdmin, admin_site


@admin.register(Industry, site=admin_site)
class IndustryAdmin(_HatchUpBaseAdmin):
    list_display = ("id", "name", "created_at", "is_active")
    search_fields = ("name",)
    date_hierarchy = "created_at"
