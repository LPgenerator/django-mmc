__author__ = 'gotlium'

from django.contrib import admin
from models import MMCLog, MMCScript, MMCHost


class MMCLogAdmin(admin.ModelAdmin):
    list_display = ('script', 'hostname', 'success', 'elapsed', 'start', 'end')
    list_filter = ('success', 'hostname', 'script', 'created',)
    list_display_links = ('script',)

    readonly_fields = (
        'start', 'end', 'elapsed', 'hostname', 'script',
        'sys_argv', 'success', 'error_message',)
    fields = (
        'start', 'end', 'elapsed', 'hostname', 'script',
        'sys_argv', 'success', 'error_message', 'traceback',)

    date_hierarchy = 'created'
    ordering = ('-id',)

    search_fields = (
        'error_message',
        'traceback'
        'hostname',
        'script',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False


class MMCBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ignore', 'created', 'id',)
    list_filter = ('created', 'ignore',)
    list_display_links = ('name',)

    readonly_fields = ('name',)

    date_hierarchy = 'created'
    ordering = ('-id',)
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MMCLog, MMCLogAdmin)
admin.site.register(MMCHost, MMCBaseAdmin)
admin.site.register(MMCScript, MMCBaseAdmin)
