# Generated by Django 2.2 on 2022-12-19 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bikingapp', '0010_auto_20221209_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]