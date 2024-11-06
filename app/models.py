from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    
    email =  models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = 'Users'

    def clean_username(self, username):
        if CustomUser.objects.filter(username=self.username).exists():
            raise ValidationError('Username already exists')
        return username
    
class Notes(TimestampModel):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name='usernotes')
    title = models.CharField(max_length=255)
    body = models.TextField()