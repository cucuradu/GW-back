from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('sensors/', views.getSensors),
    path('login/', views.user_login, name='user_login'),
    path('sensors/create/', views.createSensor),
    path('sensors/<str:pk>/update/', views.updateSensor),
    path('sensors/<str:pk>/', views.getSensor),
    path('sensors/<str:pk>/delete/', views.deleteSensor),
]