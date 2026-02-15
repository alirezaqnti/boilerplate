from django.db import models
from common.models.common_base_models import HatchUpBaseModel
from django.utils.translation import gettext_lazy as _


class Country(HatchUpBaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    phone_code = models.CharField(max_length=10, blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class Meta:
        verbose_name = "Country/Continent"
        verbose_name_plural = "Countries/Continents"
        ordering = ["name"]

    def __str__(self):
        return self.name


class City(HatchUpBaseModel):
    """
    Represents both States and Cities, as a hierarchical location model.
    If parent is null, the record is a State/province; else, it's a City under that State/province.
    """

    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        "common.Country",
        on_delete=models.CASCADE,
        related_name="administrative_divisions",
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "City/State"
        verbose_name_plural = "Cities/States"
        unique_together = ("country", "name", "parent")
        ordering = ["name"]

    def __str__(self):
        if self.parent:
            return f"{self.name}, {self.parent.name}, {self.country.name}"  # City
        else:
            return f"{self.name}, {self.country.name}"  # State/Province


class GeographicalTarget(HatchUpBaseModel):
    city = models.ForeignKey(
        "common.City",
        verbose_name=_("City"),
        related_name="cities",
        on_delete=models.CASCADE,
        limit_choices_to={"parent__isnull": False},
        blank=True,
        null=True,
    )
    state = models.ForeignKey(
        "common.City",
        verbose_name=_("State"),
        related_name="states",
        on_delete=models.CASCADE,
        limit_choices_to={"parent__isnull": True},
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        "common.Country",
        verbose_name=_("Country"),
        related_name="countries",
        on_delete=models.CASCADE,
        # Countries should be children of a continent.
        limit_choices_to={"parent__isnull": False},
        blank=True,
        null=True,
    )
    continent = models.ForeignKey(
        "common.Country",
        verbose_name=_("Continent"),
        on_delete=models.CASCADE,
        related_name="continents",
        # Continents have no parent.
        limit_choices_to={"parent__isnull": True},
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Geographical Target"
        verbose_name_plural = "Geographical Targets"
        ordering = ["country", "state", "city"]
