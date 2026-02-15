from django.contrib import admin

from users.models.users_role_models import UserRole

from common.admins.base import _HatchUpBaseAdmin, admin_site
from django.contrib.auth.admin import GroupAdmin, Group


@admin.register(Group, site=admin_site)
class GroupAdmin(GroupAdmin):
    pass


@admin.register(UserRole, site=admin_site)
class UserRoleAdmin(_HatchUpBaseAdmin):
    list_display = ("id", "user_id", "role_id", "created_at", "is_active")
    list_filter = _HatchUpBaseAdmin.list_filter + ("role_id",)
    search_fields = (
        "user_id__email",
        "user_id__first_name",
        "user_id__last_name",
        "role_id__name",
    )
    autocomplete_fields = ("user_id", "role_id")
    list_select_related = ("user_id", "role_id")
    date_hierarchy = "created_at"
