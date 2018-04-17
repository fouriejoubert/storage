# Generated by Django 2.0.1 on 2018-03-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storageadmin', '0011_auto_20180330_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storageusage',
            name='storage_usage_quota_home',
        ),
        migrations.RemoveField(
            model_name='storageusage',
            name='storage_usage_quota_lustre',
        ),
        migrations.AddField(
            model_name='profile',
            name='quota_home',
            field=models.FloatField(default=512),
        ),
        migrations.AddField(
            model_name='profile',
            name='quota_lustre',
            field=models.FloatField(default=1024),
        ),
    ]