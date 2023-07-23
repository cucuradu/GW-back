from django.contrib import admin
from .models import Record
from .models import Sensor
from .models import Plant

admin.site.register(Record)

admin.site.register(Sensor)

admin.site.register(Plant)