from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('', include('hello_world.urls'), name='hello_world'),
    path('admin/', admin.site.urls),
]
 