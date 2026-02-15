REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "common.configs.classes.common_authentication_classes.HatchupJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "common.configs.classes.common_paginators_classes.DefaultPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 10,
}
