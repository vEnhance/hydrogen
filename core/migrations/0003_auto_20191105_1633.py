# Generated by Django 2.2.7 on 2019-11-05 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191105_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='description',
        ),
        migrations.AddField(
            model_name='organization',
            name='short_description',
            field=models.TextField(default='', help_text='A short description about the contest. HTML OK.'),
        ),
        migrations.AddField(
            model_name='organization',
            name='verbose_description',
            field=models.TextField(default='', help_text='A page-long description about the contest. HTML OK.'),
        ),
    ]
