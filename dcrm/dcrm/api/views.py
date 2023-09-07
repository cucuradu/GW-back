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

plant_ranges = {
    "Tomato": {"temperature": (10.0, 30.0), "nitrogen": (20.0, 40.0), "phosphorus": (30.0, 50.0), "potassium": (32.0, 60.0)},
    "Cucumber": {"temperature": (10.0, 30.0), "nitrogen": (40.0, 60.0), "phosphorus": (20.0, 30.0), "potassium": (32.0, 45.0)},
    "Carrots": {"temperature": (15.0, 20.0), "nitrogen": (40.0, 60.0), "phosphorus": (20.0, 30.0), "potassium": (120.0, 160.0)},
    "Potatoes": {"temperature": (10.0, 35.0), "nitrogen": (100.0, 150.0), "phosphorus": (150.0, 200.0), "potassium": (200.0, 250.0)},
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

    if plant_range["temperature"][0] <= temperature <= plant_range["temperature"][1]:
       temperature_recommendation = "Temperature conditions are suitable."
    else:
        temperature_recommendation = "Temperature conditions are not optimal."

    nutrient_recommendation = []
    for nutrient, (min_range, max_range) in plant_range.items():
        if nutrient == "temperature":
            continue
        nutrient_value = getattr(sensor_reading, nutrient)
        if min_range <= nutrient_value <= max_range:
            nutrient_recommendation.append(f"{nutrient.capitalize()} level is within range.")
        else:
            nutrient_recommendation.append(f"{nutrient.capitalize()} level is not optimal.")

    return {
        "temperature_recommendation": temperature_recommendation,
        "nutrient_recommendation": nutrient_recommendation
    }


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
        recommendation = generate_recommendation(sensor, plant_ranges)
        recommendations.append({
            "sensor_data" : {
                "name": sensor.name,
                "plant": sensor.plant,
                "temperature": sensor.temperature,
                "nitrogen": sensor.nitrogen,
                "phosphorus": sensor.phosphorus,
                "potassium": sensor.potassium,
                "id": sensor.id,
            },
            "recommendation": recommendation,
        })

    return Response(recommendations)

@api_view(['PUT'])
def updateSensorData(request):
    updated_data = request.data

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
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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