from django.contrib import admin
from .models import RegisterUser, Profile, CallingDetail
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(RegisterUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(CallingDetail)