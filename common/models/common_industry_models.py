from django.db import models

from common.models.common_base_models import HatchUpBaseModel


class Industry(HatchUpBaseModel):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
