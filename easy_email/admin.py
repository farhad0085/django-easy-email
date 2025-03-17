from django.contrib import admin
from easy_email.models import Attachment, Email, Template


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'created_at', 'updated_at']


class EmailAdmin(admin.ModelAdmin):
    list_display = [
        "id", "subject", "recipients", "send_time",
        "status", "created_at", "updated_at"
    ]
    search_fields = ["subject", "recipients"]
    list_display_links = ["id", "subject"]

    def has_add_permission(self, request) -> bool:
        return False


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_display_links = ['id', 'name']


admin.site.register(Email, EmailAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Template, TemplateAdmin)
