# Generated by Django 3.0.2 on 2020-02-06 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200131_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
