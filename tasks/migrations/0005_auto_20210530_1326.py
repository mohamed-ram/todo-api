# Generated by Django 3.2.3 on 2021-05-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20210528_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='competed',
            new_name='completed',
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]