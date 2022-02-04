# Generated by Django 4.0 on 2022-02-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userfriend_unique_together_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfriend',
            constraint=models.UniqueConstraint(fields=('user_to', 'user_from'), name='unique_friends_rev_constraint'),
        ),
    ]