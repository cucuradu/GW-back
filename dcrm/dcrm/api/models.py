import random
import string
from django.db import models
from django.contrib.auth.models import User
import json

def generate_unique_id():
    """Generate a unique random 6-character ID."""
    characters = string.ascii_letters + string.digits
    while True:
        random_id = ''.join(random.choice(characters) for _ in range(6))
        if not Sensor.objects.filter(id=random_id).exists():
            return random_id

class Sensor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensors', null=True, blank=True)
    name = models.TextField(max_length=50, default="sensorName")
    plant = models.CharField(max_length=50, default="none")
    humidity = models.BooleanField(default=False)
    temperature = models.FloatField(default=0.0)
    nitrogen = models.FloatField(default=0.0)
    phosphorus = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=6, primary_key=True, default=generate_unique_id, unique=True)
    location = models.CharField(max_length=120, default="locations")

    class Meta:
        ordering = ['-updated']

class UsersTest(models.Model):
    email = models.CharField(max_length=50, default="email")
    password = models.CharField(max_length=16, default="password")
    sensors = models.ManyToManyField('Sensor', related_name='users', blank=True)
