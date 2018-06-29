# Generated by Django 2.0.6 on 2018-06-29 05:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_relation_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='relations',
        ),
        migrations.AddField(
            model_name='user',
            name='to_relation_users',
            field=models.ManyToManyField(blank=True, related_name='from_relation_users', related_query_name='from_relation_user', through='members.Relation', to=settings.AUTH_USER_MODEL),
        ),
    ]
