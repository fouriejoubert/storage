# Generated by Django 2.0.1 on 2018-01-19 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storageadmin', '0003_auto_20180118_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_date', models.DateTimeField(verbose_name='Storage date')),
                ('storage_usage_amount', models.FloatField(default=0)),
                ('storage_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StorageVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_volume_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='homestorage',
            name='home_user',
        ),
        migrations.RemoveField(
            model_name='lustrestorage',
            name='lustre_user',
        ),
        migrations.DeleteModel(
            name='HomeStorage',
        ),
        migrations.DeleteModel(
            name='LustreStorage',
        ),
        migrations.AddField(
            model_name='storageusage',
            name='storage_volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storageadmin.StorageVolume'),
        ),
    ]