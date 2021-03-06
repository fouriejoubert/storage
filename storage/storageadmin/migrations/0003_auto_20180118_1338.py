# Generated by Django 2.0.1 on 2018-01-18 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storageadmin', '0002_homestorage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homestorage',
            name='home_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lustrestorage',
            name='lustre_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
