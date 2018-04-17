from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from .models import StorageUsage
from .models import StorageVolume
from .models import BillingModel
from .models import User
from .models import Group
from .models import Profile
from datetime import datetime
import calendar
from calendar import monthrange
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

STATIC_DIR = '/var/www/html/django/static/tmp/'

def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)
        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)



@login_required
def index(request):
    all_storage_volumes = StorageVolume.objects.all()
    volume_usage_dict = {}
    volume_pie_dict = {}
    for storage_volume in all_storage_volumes:
        result = subprocess.run(['/bin/df', '-kh', storage_volume.storage_volume_path], stdout=subprocess.PIPE)
        result_string = result.stdout.decode()
        result_list = result_string.split('\n')
        if 'lustre' in storage_volume.storage_volume_path:
            (fj, total, used, free, percfree, mount_point) = result_list[1].split()
            volume_usage_dict[storage_volume.storage_volume_name] = (used, free)
        else:
            (device, total, used, free, percfree, mount_point) = result_list[1].split()
            volume_usage_dict[storage_volume.storage_volume_name] = (used, free)
        labels = ['Used', 'Free']
        used = used.replace('T', '')
        used = used.replace('G', '')
        free = free.replace('T', '')
        free = free.replace('G', '')
        sizes = []
        if 'G' in volume_usage_dict[storage_volume.storage_volume_name][0]:
            sizes.append(volume_usage_dict[storage_volume.storage_volume_name][0].replace('G', ''))
        if 'G' in volume_usage_dict[storage_volume.storage_volume_name][1]:
            sizes.append(volume_usage_dict[storage_volume.storage_volume_name][ 1].replace('G', ''))
        if 'T' in volume_usage_dict[storage_volume.storage_volume_name][0]:
            sizes.append(volume_usage_dict[storage_volume.storage_volume_name][0].replace('T', ''))
        if 'T' in volume_usage_dict[storage_volume.storage_volume_name][1]:
            sizes.append(volume_usage_dict[storage_volume.storage_volume_name][ 1].replace('T', ''))
        image_file_name = storage_volume.storage_volume_name + str(datetime.now().date()) + str(datetime.now().time()) + '.png'
        explode = (0.1, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  
        plt.show()
        fig1.savefig(STATIC_DIR + image_file_name)
        volume_pie_dict[storage_volume.storage_volume_name] = image_file_name
    context = {
        'all_storage_volumes': all_storage_volumes,
        'volume_usage_dict': volume_usage_dict,
        'volume_pie_dict': volume_pie_dict,
    }
    return render(request, 'storageadmin/index.html', context)

@login_required
def menu(request):
    return render(request, 'storageadmin/menu.html')

@login_required
def all_entries(request):
    storage_usage_records = StorageUsage.objects.order_by('id')[:]
    context = {
        'storage_usage_records': storage_usage_records,
    }
    return render(request, 'storageadmin/all_entries.html', context)

@login_required
def show_users_in_group_latest(request):
    # Deal with people that are in the admin group to only include their research group
    all_users_groups = request.user.groups.all()
    user_groups = []
    for group in all_users_groups:
        if group.name != 'admin':
            user_groups.append(group)
    the_group = user_groups[0]
    # Get all users in the group
    group_users = User.objects.filter(groups__name = user_groups[0])
    # Check if the current user is the group leader of the research group they are in        
    profile = Profile.objects.filter(user_id = request.user.id)
    # Should only be one item  - every non-admin user should only be in one research group
    # Get all the storage volumes
    storage_volumes = StorageVolume.objects.all()
    user_storage_dict = {}
    for storage_volume in storage_volumes:
            user_storage_dict[storage_volume] = []
    for users_profile in profile: 
        # If the current user is the group leader, get the latest storage usages for the members of the group
        if users_profile.groupleader == 'Yes':
            # For each user in the group, get the storage usage records for each storage volume and only report the latest entry
            for group_user in group_users:
                for storage_volume in storage_volumes:
                    user_storage_vol_dict = {}
                    user_storage_entries = StorageUsage.objects.filter(storage_user_id = group_user.id, storage_volume_id = storage_volume.id)
                    if user_storage_entries:
                        for user_storage_entry in user_storage_entries:
                            try:
                                if user_storage_entry.storage_date > user_storage_vol_dict[user_storage_entry].storage_date:
                                    # Convert to GB
                                    user_storage_entry.storage_usage_amount = user_storage_entry.storage_usage_amount * 1000 / 1000000000
                                    user_storage_vol_dict[group_user] = user_storage_entry
                            except:
                                user_storage_vol_dict[group_user] = user_storage_entry
                                # Convert to GB
                                user_storage_entry.storage_usage_amount = user_storage_entry.storage_usage_amount * 1000 / 1000000000
                        user_storage_dict[storage_volume].append(user_storage_vol_dict)
                    else:
                        new_user_storage_entry = StorageUsage()
                        new_user_storage_entry.id = 0
                        new_user_storage_entry.storage_date = datetime(1970, 1, 1)
                        new_user_storage_entry.storage_usage_amount = 0
                        new_user_storage_entry.storage_volume_id = storage_volume.id
                        user_storage_vol_dict[group_user] = new_user_storage_entry
                        user_storage_dict[storage_volume].append(user_storage_vol_dict)

 
    print(storage_volumes)
    
    context = {
        'the_group': the_group,
        'storage_volumes': storage_volumes,
        'user_storage_dict': user_storage_dict,
    }
    return render(request, 'storageadmin/show_users_in_group_latest.html', context)


@login_required
def choose_group_for_display(request):
    current_user_groups = []
    for user_s_group in request.user.groups.all():
        current_user_groups.append(user_s_group)
    for current_user_group in current_user_groups:
        if 'admin' in current_user_group.name:
            current_user_groups = Group.objects.all()
            break
    context = {
        'current_user_groups': current_user_groups,
    }
    return render(request, 'storageadmin/choose_group_for_display.html', context)

@login_required
def display_group(request, group_id):
    all_users_groups = request.user.groups.all()
    user_groups = []
    for group in all_users_groups:
        user_groups.append(group.name)
    print(user_groups)
    if 'admin' in user_groups:
        admin_user = 1
    else:
        admin_user = 0
    the_group = Group.objects.filter(id = group_id)
    group_name = the_group[0]
    group_users = User.objects.filter(groups__id = int(group_id))
    context = {
        'admin_user': admin_user,
        'group_name': group_name,
        'group_users': group_users,
    }
    return render(request, 'storageadmin/display_group.html', context)
    
    