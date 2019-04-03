# Generated by Django 2.1.7 on 2019-03-23 13:31

from django.db import migrations
from django.conf import settings
from ..serializers.datarow_serializer import DatarowSerializer
from ..serializers.dataset_serializer import DatasetSerializer
import os

# Helpers
def read_datarows(file):
    datarows = []
    with open(os.path.join(settings.BASE_DIR, file), 'r') as reader:
        for line in reader.readlines():
            datarows.append(line)
    return datarows


# Mock Operations
def mock_datarows_from_file(apps, schema_editor):
    datarows = read_datarows('texta_api/mock_data/mock_1.jl')

    for datarow in datarows:
        datarow_serializer = DatarowSerializer(data={"content": datarow})
        if datarow_serializer.is_valid():
            datarow_serializer.save()

        else:
            print('input cannot be serialized')



class Migration(migrations.Migration):

    dependencies = [
        ('texta_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(mock_datarows_from_file),
    ]