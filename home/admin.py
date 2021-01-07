from django.contrib import admin
from .models import *


class ListFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'field_label', 'list', 'status']


admin.site.register(List)
admin.site.register(ListField, ListFieldAdmin)
