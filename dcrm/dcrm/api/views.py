from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SensorSerializer
from .models import Sensor
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User


@api_view(['GET', 'POST', 'DELETE'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/dcrm/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of sensors'
        },
        {
            'Endpoint': '/dcrm/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single sensor object'
        },
        {
            'Endpoint': '/dcrm/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new sensor with data sent in post request'
        },
        {
            'Endpoint': '/dcrm/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing sensor with data sent in put request'
        },
        {
            'Endpoint': '/dcrm/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting sensor'
        }
    ]
    return Response(routes)

@api_view(['GET'])
def getSensors(request):
    sensors = Sensor.objects.all()
    serializer = SensorSerializer(sensors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSensor(request, pk):
    sensor = Sensor.objects.get(id=pk)
    serializer = SensorSerializer(sensor, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createSensor(request):
    data = request.data

    sensor_name = data.get('name', None)
    sensor_humidity = data.get('humidity', False)
    sensor_temperature = data.get('temperature', 0.0)
    sensor_nitrogen = data.get('nitrogen', 0.0)
    sensor_phosphorus = data.get('phosphorus', 0.0)
    sensor_potassium = data.get('potassium', 0.0)

    sensor = Sensor.objects.create(
        name = sensor_name,
        humidity = sensor_humidity,
        temperature = sensor_temperature,
        nitrogen = sensor_nitrogen,
        phosphorus = sensor_phosphorus,
        potassium = sensor_potassium
    )

    serializer = SensorSerializer(sensor, many=False)
    return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['PUT'])
def updateSensor(request, pk):
    try:
        sensor = Sensor.objects.get(pk=pk)
    except Sensor.DoesNotExist:
        return Response({"error": "Sensor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data

    sensor.humidity = data.get('humidity', sensor.humidity)
    sensor.temperature = data.get('temperature', sensor.temperature)
    sensor.nitrogen = data.get('nitrogen', sensor.nitrogen)
    sensor.phosphorus = data.get('phosphorus', sensor.phosphorus)
    sensor.potassium = data.get('potassium', sensor.potassium)
    sensor.save()

    serializer = SensorSerializer(sensor, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteSensor(request, pk):

    sensor = Sensor.objects.get(pk=pk)
    serializer = SensorSerializer(sensor, many=False)

    sensor.delete()
    return Response(serializer.data)

@api_view(['GET'])
def getRecommendation(request):
    sensors = Sensor.objects.all()
    recommandations = []

    for sensor in sensors:
        if not sensor.humidity:
            recommandation = f"For sensor '{sensor.name}': Very low humidity level. Please take necessary actions."

        recommandations.append(recommandation)

    response_data = {"recomandations": recommandations}
    return Response(response_data)

# class UserRecordView(APIView):
#     """
#     API View to create or get a list of all the registered users.
#     GET request returns the registered users whereas a POST request
#     allows to create a new user.
#     """
#     permission_classes = [IsAdminUser]

#     def get(self, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=ValueError):
#             serializer.create(validated_data=request.data)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             {
#                 "error": True,
#                 "error_msg": serializer.error_messages,
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )