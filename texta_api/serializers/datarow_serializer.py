from rest_framework import serializers

from texta_api.models.datarow_model import Datarow

class DatarowSerializer(serializers.ModelSerializer):
    content = serializers.CharField()

    class Meta:
        model = Datarow
        fields = '__all__'
