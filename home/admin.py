from django.contrib import admin
from .models import *


class ListAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'app', 'created_at', 'created_user', 'last_updated', 'status']


class ListFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'list', 'field_id', 'field_label', 'field_type', 'select_list', 'primary', 'required', 'visible', 'order', 'created_at', 'created_user', 'last_updated', 'status']


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'list', 'created_at', 'created_user', 'last_updated', 'status']


class RecordFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'record', 'list_field', 'list_field_id', 'value', 'selected_record', 'created_at', 'created_user', 'last_updated', 'status']

    def list_field_id(self, obj):
        try:
            return obj.list_field.id
        except:
            pass

admin.site.register(List, ListAdmin)
admin.site.register(ListField, ListFieldAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RecordField, RecordFieldAdmin)
