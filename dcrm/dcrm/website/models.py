from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")

class Plant(models.Model):
    usual_name = models.CharField(max_length=50)
    latin_name = models.CharField(max_length=50)
    sodium_level = models.FloatField()
    potassium_level = models.FloatField()
    ph_levels = models.FloatField()
    temperature = models.FloatField()
    humidity_level=models.FloatField()
    
    def __str__(self):
        return (f"{self.usual_name}")

class Sensor(models.Model):
    sensor_location = models.CharField(max_length=100)
    sensor_name = models.CharField(max_length=50)
    sensor_type = models.CharField(max_length=50)
    sensor_info_temperature = models.FloatField()
    sensor_info_humidity = models.FloatField()

    def __str__(self):
        return(f"{self.sensor_name} {self.sensor_type}")


        