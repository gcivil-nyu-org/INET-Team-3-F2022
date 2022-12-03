# Generated by Django 2.2 on 2022-12-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikingapp', '0005_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='latitude',
            field=models.DecimalField(decimal_places=5, max_digits=6),
        ),
        migrations.AlterField(
            model_name='issue',
            name='longitude',
            field=models.DecimalField(decimal_places=5, max_digits=6),
        ),
    ]
