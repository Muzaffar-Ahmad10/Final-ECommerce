from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('', include('mainapp.urls'), name='mainapp'),
    path('products/', include('products.urls'), name='products'),
    path('cart/', include('cart.urls'), name='cart'),
    path('admin/', admin.site.urls),
]
 