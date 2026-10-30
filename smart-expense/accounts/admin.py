from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from audit.models import AuditEvent

from .models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        AuditEvent.objects.create(actor=request.user, event="admin_user_changed" if change else "admin_user_created")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        AuditEvent.objects.create(actor=request.user, event="admin_user_deleted")

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        AuditEvent.objects.create(actor=request.user, event="admin_users_deleted")
