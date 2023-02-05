from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Comment(models.Model):
    content_id = models.BigIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_id) + '-' + self.body[:15]
