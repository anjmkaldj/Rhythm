# Generated by Django 5.0.6 on 2024-06-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0003_karoakedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='karoakedetails',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
