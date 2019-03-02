from django.urls import path
from app.views import views

app_name = 'app'

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
]
