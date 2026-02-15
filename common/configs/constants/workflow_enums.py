from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkflowScopeChoices(models.TextChoices):
    ADMIN = "admin", _("Admin")
    INVESTOR = "investor", _("Investor")
    STARTUP = "startup", _("Startup")
