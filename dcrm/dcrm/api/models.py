from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    #Custom fields
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Specify unique related names for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username


class Sensor(models.Model):
    name = models.TextField(max_length=50)
    humidity = models.BooleanField(default=False)
    temperature = models.FloatField(default=0.0)
    npk = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated']