from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_title', 'description']
    list_filter = ['title']
    
    def task_title(self, obj):
        return obj.title.title()

