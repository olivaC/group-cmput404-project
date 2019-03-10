from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('verify_login/', views.verify_login, name="verify_login"),
    path('verify_register/', views.verify_register, name="verify_register"),
    path('index/<str:username>', views.index, name="index"),
]
