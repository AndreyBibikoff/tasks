from django.contrib import admin

# Register your models here.
from task.models import TaskUser

admin.site.register(TaskUser)
