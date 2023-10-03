from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SensorSerializer
from .models import Sensor
from .serializers import UserTestSerializer
from .models import UsersTest
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
import json


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

plant_ranges = {
    "Tomato": {"temperature": (10.0, 30.0), "nitrogen": (40.0, 60.0), "phosphorus": (30.0, 50.0), "potassium": (40.0, 70.0)},
    "Cucumber": {"temperature": (10.0, 30.0), "nitrogen": (40.0, 60.0), "phosphorus": (30.0, 50.0), "potassium": (40.0, 70.0)},
    "Carrots": {"temperature": (10.0, 30.0), "nitrogen": (40.0, 60.0), "phosphorus": (30.0, 50.0), "potassium": (40.0, 70.0)},
    "Potatoes": {"temperature": (10.0, 30.0), "nitrogen": (40.0, 60.0), "phosphorus": (30.0, 50.0), "potassium": (40.0, 70.0)},
    
}

def generate_recommendation(sensor_reading, plant_ranges):

    plant_name = sensor_reading.plant
    plant_range = plant_ranges.get(plant_name) 

    if not plant_range:
        return "Plant type not found."
    
    temperature = sensor_reading.temperature
    nitrogen = sensor_reading.nitrogen
    phosphorus =sensor_reading.phosphorus
    potassium = sensor_reading.potassium
    humidity = sensor_reading.humidity

    problem_count = 0

    if humidity:
        humidity_recommendation = "Humidity is okay"
        problem_count = 0
    else:
        humidity_recommendation = "Humidity is low. Consider increasing humidity levels."
        problem_count += 1


    if plant_range["temperature"][0] <= temperature <= plant_range["temperature"][1]:
       temperature_recommendation = "Temperature conditions are suitable."
    else:
        temperature_recommendation = "Temperature conditions are not optimal."
        problem_count += 1

    nutrient_recommendation = []
    for nutrient, (min_range, max_range) in plant_range.items():
        if nutrient == "temperature" or nutrient == "humidity":
            continue
        nutrient_value = getattr(sensor_reading, nutrient)
        if min_range <= nutrient_value <= max_range:
            nutrient_recommendation.append(f"{nutrient.capitalize()} level is within range.")
        else:
            nutrient_recommendation.append(f"{nutrient.capitalize()} level is not optimal.")
            problem_count += 1

    return {
        "humidity_recommendation": humidity_recommendation,
        "temperature_recommendation": temperature_recommendation,
        "nutrient_recommendation": nutrient_recommendation
    }, problem_count


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
    recommendations = []

    for sensor in sensors:
        recommendation, problem_count = generate_recommendation(sensor, plant_ranges)
        recommendations.append({
            "sensor_data" : {
                "name": sensor.name,
                "plant": sensor.plant,
                "temperature": sensor.temperature,
                "humidity": sensor.humidity,
                "nitrogen": sensor.nitrogen,
                "phosphorus": sensor.phosphorus,
                "potassium": sensor.potassium,
                "id": sensor.id,
            },
            "recommendation": recommendation,
            "problem_count": problem_count
        })

    return Response(recommendations)

@api_view(['GET'])
def get_location_by_sensor_id(request, sensor_id):
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Extract the location from the sensor
    location = sensor.location

    return Response({'location': location}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_location_to_sensor(request, sensor_id):
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Extract the location data from the request data
    location = request.data.get('location', '')

    # Update the sensor's location field
    sensor.location = location
    sensor.save()

    # Serialize the updated sensor and return it in the response
    serializer = SensorSerializer(sensor)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateSensorData(request):
    updated_data = request.data

    if not isinstance(updated_data, list):
        return Response({"error": "Invalid input data format."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        for update_entry in updated_data:
            sensor_data = update_entry.get('sensor_data')

            sensor_id = sensor_data.get('id')
            if sensor_id is None:
                return Response({"error": "Sensor ID is missing in the update data."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sensor = Sensor.objects.get(id=sensor_id)
            except Sensor.DoesNotExist:
                return Response({"error": f"Sensor with ID {sensor_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            sensor.name = sensor_data.get('name', sensor.name)
            sensor.plant = sensor_data.get('plant', sensor.plant)
            sensor.save()

        return Response({"message": "Sensor data updated successfully."}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def usersData(request, id):
    try:
        user = UsersTest.objects.get(pk=id)
    except UsersTest.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserTestSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addSensorsToUser(request, user_id):
    try:
        user = UsersTest.objects.get(id=user_id)
    except UsersTest.DoesNotExist:
        return Response({'message': 'User not found.'}, status=404)
    
    sensor_ids = request.data.get('sensor_ids', [])

    for sensor_id in sensor_ids:
        try:
            sensor = Sensor.objects.get(id=sensor_id)
            user.sensors.add(sensor)

        except Sensor.DoesNotExist:
            return Response({'message': f'Sensor with ID {sensor_id} not found.'}, status=404)

    user.save()
    return Response({'message': f'Sensors added to user {user_id}.'}, status=200)

@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    email = data.get('email', None)
    password = data.get('password', None)
    
    if email is None or password is None:
        return Response({'message': 'Email and password are required.'}, status=400)
    
    try:
        user = UsersTest.objects.get(email=email)
    except UsersTest.DoesNotExist:
        return Response({'message': 'User not found.'}, status=404)
    
    if user.password == password:
        serializer = UserTestSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Authentication failed.'}, status=401)



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