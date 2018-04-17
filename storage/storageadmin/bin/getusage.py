#!/usr/local/bin/python3

import os
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storage.settings")
import django
from django.utils import timezone
django.setup()
from storageadmin.models import StorageVolume, StorageUsage, User, Profile


def UserNotFound(username):
    print('User not found: ' + username)

def AddStorageRecord(username, storage_usage_amount, storage_volume_name):
    u = User.objects.get(username = username)
    v = StorageVolume.objects.get(storage_volume_name = storage_volume_name)
    q = StorageUsage(storage_user = u, storage_volume = v, storage_date = timezone.now(), storage_usage_amount = storage_usage_amount)
    q.save()


def GetXFSStorageUsage(fqvolume):
    xfs_storage_usage_list = []
    result = subprocess.run(['/usr/sbin/xfs_quota', '-xc', 'report', '/home'], stdout=subprocess.PIPE)
    result_string = result.stdout.decode()
    result_list = result_string.split('\n')
    for line in result_list:
        if line.startswith("Group quota"):
                break
        if line.startswith("User") or line.startswith(" ") or line.startswith("\n")  or line.startswith("-"):
                pass
        else:
                xfs_storage_usage_list.append(line.rstrip("\n"))
    for line in xfs_storage_usage_list:
        if line != '':
            (username, storage_usage_amount, none1, none2, none3, none4) = line.split()
            try:
                add_storage_record_result = AddStorageRecord(username, storage_usage_amount, 'home')
            except:
                UserNotFound(username)


def GetLustreStorageUsage(fqvolume):
    lustre_storage_usage_list = []
    u = User.objects.all()
    u = ['fourie']
    for username in u:
        result = subprocess.run(['/usr/bin/lfs', 'quota', '-u', username, fqvolume], stdout=subprocess.PIPE)
        print(result)
        result_string = result.stdout.decode()
        result_list = result_string.split('\n')
        for line in result_list:
                if ("Disk" in line) or ("Filesystem" in line):
                        pass
                else:
                        lustre_storage_usage_list.append(line.rstrip("\n"))
        for line in lustre_storage_usage_list:
            if line != '':
                (fs, storage_usage_amount, b, c, d, e, f, g, h) = line.split()
                try:
                    add_storage_record_result = AddStorageRecord(username, storage_usage_amount, 'lustre')
                except:
                    UserNotFound(username)
        
                        
                        
                        

GetLustreStorageUsage('/lustre')

GetXFSStorageUsage('/home')


