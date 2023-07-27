from django.db import models

class Sensor(models.Model):
    name = models.TextField(max_length=50)
    humidity = models.BooleanField(default=False)
    temperature = models.FloatField(default=0.0)
    npk = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-updated']