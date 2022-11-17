# Generated by Django 2.2 on 2022-11-16 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bikingapp", "0015_auto_20221114_1726"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventFriendMgmt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="bikingapp.Event",
                    ),
                ),
                (
                    "friend",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="friends2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]