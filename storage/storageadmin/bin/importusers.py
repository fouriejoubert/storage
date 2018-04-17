#!/usr/local/bin/python3

import os
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storage.settings")
import django
from django.utils import timezone
django.setup()
from storageadmin.models import StorageVolume, StorageUsage, User, Group, Profile

#INFILE = "/usr/local/storage/users_and_groups.txt"

INFILE = "/usr/local/storage/users.txt"
existingusers = User.objects.all()
prev = []
for i in existingusers:
    prev.append(i.username)

fh = open(INFILE, 'r')

for line in fh.readlines():
    (username, first_name, last_name, email, group_name) = line.rstrip('\n').split('\t')
    if username in prev:
        print(username + ' already exists...')
    else:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password='genomics')
        my_group = Group.objects.get(name=group_name)
        my_group.user_set.add(user)
    
fh.close()
