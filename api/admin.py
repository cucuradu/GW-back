from django.contrib import admin

# Register your models here.

from .models import Sensor
from .models import UsersTest

admin.site.register(Sensor)
admin.site.register(UsersTest)