from rest_framework.serializers import ModelSerializer
from .models import Sensor


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'