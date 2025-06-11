from django.contrib import admin

# Register your models here.
from .models import Tasks


class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Tasks,TasksAdmin)