# Generated by Django 3.1.7 on 2021-05-28 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='competed',
            field=models.BooleanField(default=False),
        ),
    ]
