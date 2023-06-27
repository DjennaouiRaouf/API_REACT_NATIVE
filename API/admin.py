from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


lpp=20
class CustomUserAdmin(UserAdmin):
    list_display = ['user_id','username','phone_number','email','type','is_active']
    list_per_page = lpp
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','phone_number','type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                                    'otp_enabled','otp_verified','otp_base32','otp_auth_url')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserAccount, CustomUserAdmin)


class CustomGroupAdmin(GroupAdmin):
    list_display = ['group_id','name']
    pass

admin.site.unregister(Group)
admin.site.register(GroupUser, CustomGroupAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id','store_name','manager','longitude','latitude','is_available']


admin.site.register(Store,StoreAdmin)

