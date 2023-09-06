import random
import string
from django.db import models

def generate_unique_id():
    """Generate a unique random 6-character ID."""
    characters = string.ascii_letters + string.digits
    while True:
        random_id = ''.join(random.choice(characters) for _ in range(6))
        if not Sensor.objects.filter(id=random_id).exists():
            return random_id

class Sensor(models.Model):
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
    
    class Meta:
        ordering = ['-updated']