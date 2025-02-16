# Generated by Django 5.0.6 on 2024-06-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_remove_userreg_g'),
    ]

    operations = [
        migrations.CreateModel(
            name='karoakedetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='images/')),
                ('des', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
    ]
