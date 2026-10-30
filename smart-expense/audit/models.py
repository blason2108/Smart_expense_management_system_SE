from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    event = models.CharField(max_length=50)

    class Meta:
        ordering = ["-timestamp"]
