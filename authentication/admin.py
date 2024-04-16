from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Users

admin.site.register(Users)
admin.site.unregister(Group)