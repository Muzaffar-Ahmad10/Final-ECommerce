from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("dashboard/", dashboard, name="dashboard"),
    path("signup/", signup_user, name="signup"),
    path("login/", login_user, name="login"),
    path("hot-products/", hot_products, name="host_products"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add-product/', add_product, name='add_product'),
    path('inventory/', inventory, name='inventory'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', single_product, name='single_product'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('my-orders/', my_orders, name='my_orders'),
    path('view-bill/<int:transaction_id>/', view_bill, name='view_bill'),
    path('all-orders/', all_orders, name='all_orders'),
    path('contact-us/', contact_us_submit, name='contact_us'),
    path('change-password/', change_password, name='change_password'),
    path('privacy-policy/', privacy, name='privacy'),
    path('about-us/', about_us, name='about_us'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)