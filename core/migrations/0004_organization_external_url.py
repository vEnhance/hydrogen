# Generated by Django 2.2.7 on 2019-11-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191105_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='external_url',
            field=models.CharField(blank=True, default='', help_text='A website to link to.', max_length=80),
        ),
    ]
