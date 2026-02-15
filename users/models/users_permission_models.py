from django.contrib.auth.models import PermissionsMixin as DjangoPermissionsMixin


class PermissionsMixin(DjangoPermissionsMixin):
    """
    Compatibility wrapper around Django's default permissions mixin.
    """

    class Meta:
        abstract = True
