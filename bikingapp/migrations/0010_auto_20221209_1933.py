# Generated by Django 2.2 on 2022-12-10 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bikingapp", "0009_merge_20221205_1622"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="issue",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="issue",
            name="longitude",
        ),
        migrations.AddField(
            model_name="issue",
            name="location",
            field=models.CharField(default="NYU Tandon", max_length=100),
        ),
    ]