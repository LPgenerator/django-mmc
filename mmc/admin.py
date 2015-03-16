__author__ = 'gotlium'

from django.contrib import admin
from models import MMCLog, MMCScript, MMCHost, MMCEmail


class MMCLogAdmin(admin.ModelAdmin):
    list_display = (
        'script', 'hostname', 'success', 'elapsed',
        'memory', 'cpu_time', 'start', 'end')
    list_filter = ('success', 'hostname', 'script', 'created',)
    list_display_links = ('script',)

    readonly_fields = (
        'start', 'end', 'elapsed', 'hostname', 'script',
        'sys_argv', 'success', 'error_message', 'memory', 'cpu_time')
    fields = (
        'start', 'end', 'elapsed', 'hostname', 'script', 'memory', 'cpu_time',
        'sys_argv', 'success', 'error_message', 'traceback', 'stdout_messages')

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


class MMCHostAdmin(admin.ModelAdmin):
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


class MMCScriptAdmin(MMCHostAdmin):
    list_display = (
        'name', 'ignore', 'one_copy', 'save_on_error', 'created', 'id',)
    list_filter = ('ignore', 'one_copy', 'save_on_error')
    fieldsets = [
        ('Basic', {'fields': [
            'ignore', 'one_copy', 'save_on_error'
        ]}),
        ('Triggers', {'fields': [
            'enable_triggers', 'trigger_time', 'trigger_memory', 'trigger_cpu'
        ]}),
    ]


class MMCEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created', 'id',)
    list_filter = ('created', 'is_active',)
    list_display_links = ('email',)
    filter_horizontal = ('ignore',)

    date_hierarchy = 'created'
    ordering = ('-id',)
    search_fields = ('email',)


admin.site.register(MMCLog, MMCLogAdmin)
admin.site.register(MMCHost, MMCHostAdmin)
admin.site.register(MMCScript, MMCScriptAdmin)
admin.site.register(MMCEmail, MMCEmailAdmin)
