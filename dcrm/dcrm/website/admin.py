from django.contrib import admin
from .models import Record
from .models import Sensor

admin.site.register(Record)

admin.site.register(Sensor)
