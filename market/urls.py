from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login
app_name = 'robot'
urlpatterns = [
    path('', views.reviewIndex, name='index'),
    path('json/', views.getJson, name='getJson'),
    path('login/', login, {'template_name': 'html/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('waves/', views.waves, name='waves')
]
