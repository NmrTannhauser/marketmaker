#from django.conf.urls import url
#from django.contrib import admin
from django.urls import path ,include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market.urls', namespace='robot')),
]
