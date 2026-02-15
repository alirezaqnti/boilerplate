from django.contrib import admin

from common.models.common_region_models import (
    City,
    Country,
    GeographicalTarget,
)

from common.admins.base import _HatchUpBaseAdmin, admin_site


@admin.register(Country, site=admin_site)
class CountryAdmin(_HatchUpBaseAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "phone_code",
        "parent",
        "created_at",
        "is_active",
    )
    search_fields = ("name", "code", "phone_code", "parent__name")
    autocomplete_fields = ("parent",)
    list_select_related = ("parent",)
    date_hierarchy = "created_at"


@admin.register(City, site=admin_site)
class CityAdmin(_HatchUpBaseAdmin):
    list_display = (
        "id",
        "name",
        "country",
        "parent",
        "code",
        "created_at",
        "is_active",
    )
    list_filter = _HatchUpBaseAdmin.list_filter + ("country",)
    search_fields = ("name", "code", "country__name", "parent__name")
    autocomplete_fields = ("country", "parent")
    list_select_related = ("country", "parent")
    date_hierarchy = "created_at"


@admin.register(GeographicalTarget, site=admin_site)
class GeographicalTargetAdmin(_HatchUpBaseAdmin):
    list_display = (
        "id",
        "country",
        "state",
        "city",
        "continent",
        "created_at",
        "is_active",
    )
    list_filter = _HatchUpBaseAdmin.list_filter + ("country", "state", "continent")
    search_fields = (
        "country__name",
        "state__name",
        "city__name",
        "continent__name",
    )
    autocomplete_fields = ("country", "state", "city", "continent")
    list_select_related = ("country", "state", "city", "continent")
    date_hierarchy = "created_at"
