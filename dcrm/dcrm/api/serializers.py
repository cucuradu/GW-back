from rest_framework.serializers import ModelSerializer
from .models import Sensor
from django.contrib.auth.models import User
from rest_framework import serializers


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        