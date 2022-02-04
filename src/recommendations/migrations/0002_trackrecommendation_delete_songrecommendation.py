# Generated by Django 4.0 on 2022-02-04 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spotify_track_id', models.CharField(max_length=128)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_recommendation_from', to='auth.user')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_recommendation_to', to='auth.user')),
            ],
            options={
                'verbose_name': 'track recommendations',
                'verbose_name_plural': 'track recommendations',
            },
        ),
        migrations.DeleteModel(
            name='SongRecommendation',
        ),
    ]
