from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define the extended user model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    is_group_leader = models.BooleanField(default = False)
    quota_home = models.FloatField(default = 512)
    usage_home = models.FloatField(default = 512)
    quota_lustre = models.FloatField(default = 1024)
    usage_lustre = models.FloatField(default = 1024)
    quota_galaxy = models.FloatField(default = 512)
    usage_galaxy = models.FloatField(default = 512)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Define the storage volume model

class StorageVolume(models.Model):
    storage_volume_name = models.CharField(max_length = 30)
    storage_volume_path = models.CharField(max_length = 30)

# Define the storage usage model

class StorageUsage(models.Model):
    storage_user = models.ForeignKey(User, on_delete = models.PROTECT)
    storage_volume = models.ForeignKey(StorageVolume, on_delete = models.PROTECT)
    storage_date = models.DateTimeField('Storage date')
    storage_usage_amount = models.FloatField(default = 0)

# Define the billing model

class BillingModel(models.Model):
    cost_per_tb_per_day = models.FloatField(default = 0)
