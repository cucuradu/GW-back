from rest_framework.serializers import ModelSerializer
from .models import Sensor
from .models import UsersTest
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTest
        fields = '__all__'
        