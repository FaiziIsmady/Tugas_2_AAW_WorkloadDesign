from django.db import models


class BroadcastMessage(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    message = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    last_action = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.external_id} ({self.last_action})"


class ConsumerEventLog(models.Model):
    event_type = models.CharField(max_length=64)
    message_id = models.CharField(max_length=64)
    payload = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-processed_at"]

    def __str__(self):
        return f"{self.event_type} - {self.message_id}"
