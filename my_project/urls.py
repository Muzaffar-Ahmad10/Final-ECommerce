from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from .sitemap import PostSitemap, ProductSitemap
from mainapp.views import custom_page_not_found_view
from django.conf.urls import handler404

handler404 = custom_page_not_found_view

sitemaps = {
    'posts': PostSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('', include('mainapp.urls'), name='mainapp'),
    path('products/', include('products.urls'), name='products'),
    path('cart/', include('cart.urls'), name='cart'),
    path('admin/', admin.site.urls),
]
 