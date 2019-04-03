# Generated by Django 2.1.7 on 2019-03-25 15:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('texta_api', '0004_dataset_rows'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarow',
            name='dataset_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='texta_api.Dataset'),
            preserve_default=False,
        ),
    ]
