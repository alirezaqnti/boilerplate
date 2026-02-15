from django.contrib import admin

from users.models.users_user_models import User

from common.admins.base import _HatchUpBaseAdmin, admin_site


@admin.register(User, site=admin_site)
class UserAdmin(_HatchUpBaseAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "phone_number",
        "is_superuser",
        "is_active",
        "created_at",
    )
    list_filter = _HatchUpBaseAdmin.list_filter + ("is_superuser",)
    search_fields = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )
    date_hierarchy = "created_at"
