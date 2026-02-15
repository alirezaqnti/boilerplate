from rest_framework import serializers

from common.models.common_industry_models import Industry


class IndustrySerializers(serializers.ModelSerializer):

    class Meta:
        model = Industry
        fields = ["id", "name"]
