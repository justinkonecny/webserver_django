# Generated by Django 4.0 on 2022-08-06 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0002_trackrecommendation_delete_songrecommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackrecommendation',
            name='has_listened',
            field=models.BooleanField(default=False),
        ),
    ]