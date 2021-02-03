from django.contrib import admin

# Register your models here.
from task.models import NormalUser, AdminUser

admin.site.register(NormalUser)
admin.site.register(AdminUser)