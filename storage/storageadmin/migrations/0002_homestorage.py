# Generated by Django 2.0.1 on 2018-01-10 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storageadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_date', models.DateTimeField(verbose_name='Home storage date')),
                ('home_usage', models.FloatField(default=0)),
                ('home_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
