from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User
from .models import *


lpp=20
class CustomUserAdmin(UserAdmin):
    list_display = ['user_id','username','phone_number','email','type','is_active']
    list_per_page = lpp
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','phone_number','type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserAccount, CustomUserAdmin)


class CustomGroupAdmin(GroupAdmin):
    list_display = ['group_id','name']
    pass

admin.site.unregister(Group)
admin.site.register(GroupUser, CustomGroupAdmin)