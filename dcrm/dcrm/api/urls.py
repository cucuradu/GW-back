from django.urls import path
from . import views
from .views import UserRecordView

app_name = 'api'
urlpatterns = [
    path('', views.getRoutes),
    path('user/', UserRecordView.as_view(), name='users'),
    path('sensors/', views.getSensors),
    path('sensors/create/', views.createSensor),
    path('sensors/<str:pk>/update/', views.updateSensor),
    path('sensors/<str:pk>/', views.getSensor),
    path('sensors/<str:pk>/delete/', views.deleteSensor),
    path('api/recommendations/', views.getRecommendation, name='recommendations')
]