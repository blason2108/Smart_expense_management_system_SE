from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import AuditEvent


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    AuditEvent.objects.create(actor=user, event="login")


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    AuditEvent.objects.create(actor=user, event="logout")


@receiver(user_login_failed)
def on_failure(sender, credentials, request, **kwargs):
    # Deliberately never persist credentials, username, or request body.
    AuditEvent.objects.create(event="login_failed")
