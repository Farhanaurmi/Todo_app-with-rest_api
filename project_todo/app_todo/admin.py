from django.contrib import admin
from .models import TodoClass
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('Ctime',)

admin.site.register(TodoClass, TodoAdmin)