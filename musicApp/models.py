from django.db import models
from django.contrib.auth.models import User

VISIBILITY_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private'),
    ('protected', 'Protected'),
)

class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='music')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    allowed_emails = models.TextField(blank=True)

    def __str__(self):
        return self.title