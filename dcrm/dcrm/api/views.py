from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SensorSerializer
from .models import Sensor
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

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

    sensor = Sensor.objects.create(
        name=data['name']
    )
    serializer = SensorSerializer(sensor, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateSensor(request, pk):
    data = request.data

    sensor = Sensor.objects.get(id=pk)
    serializer = SensorSerializer(sensor, data=request.POST)
    if serializer.is_valid():
        
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteSensor(request, pk):

    sensor = Sensor.objects.get(pk=pk)
    serializer = SensorSerializer(sensor, many=False)

    sensor.delete()
    return Response(serializer.data)

@api_view(['POST'])
def user_login(request):
    User = get_user_model()

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.get(username=username)

    if user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)