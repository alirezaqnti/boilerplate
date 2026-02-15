from rest_framework import serializers

from common.models.common_region_models import City, Country, GeographicalTarget


class _BaseCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "code"]


class CitySerializer(_BaseCitySerializer):
    parent = _BaseCitySerializer()

    class Meta:
        model = City
        fields = ["id", "name", "parent"]


class GeographicalTargetSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.filter(parent__isnull=False),
        required=False,
    )
    state = serializers.PrimaryKeyRelatedField(
        required=False, queryset=City.objects.filter(parent__isnull=True)
    )
    country = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Country.objects.filter(parent__isnull=False)
    )
    continent = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Country.objects.filter(parent__isnull=True)
    )

    class Meta:
        model = GeographicalTarget
        fields = [
            "city",
            "state",
            "country",
            "continent",
        ]
