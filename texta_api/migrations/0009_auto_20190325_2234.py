# Generated by Django 2.1.7 on 2019-03-25 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texta_api', '0008_auto_20190325_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='rows',
            field=models.TextField(blank=True, null=True),
        ),
    ]
