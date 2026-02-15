from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.models.common_base_models import HatchUpBaseModel


class Tag(HatchUpBaseModel):
    """
    Tag with a category/type to distinguish which entity it applies to.
    """

    class TagType(models.TextChoices):
        STARTUP = "startup", _("Startup")
        INVESTOR = "investor", _("Investor")
        DOCUMENT = "document", _("Document")
        USER = "user", _("User")
        CUSTOMER_SEGMENT = "customer_segment", _("Customer segment")
        OTHER = "other", _("Other")

    type = models.CharField(
        max_length=32,
        choices=TagType.choices,
        default=TagType.OTHER,
        db_index=True,
    )
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=80, blank=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"],
                name="uq_common_tag_type_name",
            ),
            models.UniqueConstraint(
                fields=["type", "slug"],
                name="uq_common_tag_type_slug",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.type}: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
