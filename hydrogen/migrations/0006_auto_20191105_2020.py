# Generated by Django 2.2.7 on 2019-11-06 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydrogen', '0005_auto_20191105_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='time_limit',
            field=models.PositiveIntegerField(default=0, help_text='How long is the contest in minutes? Choose 0 for no time limit at all.'),
        ),
    ]
