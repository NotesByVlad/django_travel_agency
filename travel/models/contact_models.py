from django.db import models
from django.conf import settings
from django.utils import timezone

class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Admin reply fields
    reply_message = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email} at {self.created_at:%Y-%m-%d %H:%M}"
    
    def save(self, *args, **kwargs):
        if self.reply_message and not self.replied:
            self.replied = True
            self.replied_at = timezone.now()
        elif not self.reply_message:
            self.replied = False
            self.replied_at = None
        super().save(*args, **kwargs)