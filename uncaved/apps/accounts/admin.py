from django.contrib import admin

# Register your models here.

from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'  # Specify the foreign key field name

# register the Profile model with the User model
admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, UserAdmin)  # Register the User model with the custom Profile inline
UserAdmin.inlines = (ProfileInline,)