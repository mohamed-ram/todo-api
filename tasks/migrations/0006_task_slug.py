# Generated by Django 3.2.3 on 2021-05-31 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210530_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
