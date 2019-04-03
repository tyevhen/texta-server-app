from rest_framework import serializers

from texta_api.models.dataset_model import Dataset

from texta_api.serializers.datarow_serializer import DatarowSerializer


class DatasetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, allow_null=False)
    rows = serializers.CharField(default='[]')

    class Meta:
        model = Dataset
        fields = '__all__'
