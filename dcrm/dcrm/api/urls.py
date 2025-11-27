from django.urls import path
from . import views
from .auth_views import RegisterView, UserProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'apiRest'
urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # Existing endpoints
    path('', views.getRoutes),
    path('sensors/', views.getSensors),
    path('sensors/create/', views.createSensor),
    path('sensors/<str:pk>/update/', views.updateSensor),
    path('sensors/<str:pk>/', views.getSensor),
    path('sensors/<str:pk>/delete/', views.deleteSensor),
    path('sensor/add_location/<str:sensor_id>/', views.add_location_to_sensor, name='add_location_to_sensor'),
    path('sensor/get_location/<str:sensor_id>/', views.get_location_by_sensor_id, name='get_location_by_sensor_id'),
    path('apiRest/recommendations/', views.getRecommendation),
    path('api/update_sensors/', views.updateSensorData, name='update_sensor'),
    path('api/user/<int:id>', views.usersData, name='get_user'),
    path('api/add_sensors_to_user/<str:user_id>/', views.addSensorsToUser, name='add_sensors_to_user'),
    path('api/authenticate/', views.authenticate_user, name='authenticate_user'),
]
