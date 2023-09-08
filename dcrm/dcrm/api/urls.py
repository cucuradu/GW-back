from django.urls import path
from . import views
# from .views import UserRecordView

app_name = 'apiRest'
urlpatterns = [
    path('', views.getRoutes),
    #path('user/', UserRecordView.as_view(), name='users'),
    path('sensors/', views.getSensors),
    path('sensors/create/', views.createSensor),
    path('sensors/<str:pk>/update/', views.updateSensor),
    path('sensors/<str:pk>/', views.getSensor),
    path('sensors/<str:pk>/delete/', views.deleteSensor),
    path('apiRest/recommendations/', views.getRecommendation),
    path('api/update_sensors/', views.updateSensorData, name='update_sensor'),
    path('api/users/', views.usersData, name='get_users'),
    path('api/authenticate/', views.authenticate_user, name='authenticate_user'),
]
