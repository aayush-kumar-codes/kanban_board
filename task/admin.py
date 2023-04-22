from django.contrib import admin

from .models import Task, Board

# Register your models here.
admin.site.register(Task)
admin.site.register(Board)