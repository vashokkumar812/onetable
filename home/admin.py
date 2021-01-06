from django.contrib import admin
from .models import *


class ListFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'field_label', 'list']


admin.site.register(List)
admin.site.register(ListField, ListFieldAdmin)
