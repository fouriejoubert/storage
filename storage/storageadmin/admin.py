from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import StorageVolume
from .models import StorageUsage
from .models import Profile



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class ProfileAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )    


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(StorageVolume)
admin.site.register(StorageUsage)
admin.site.register(Profile)
