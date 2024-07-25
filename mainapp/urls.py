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
    path('my-orders/', my_orders, name='my_orders'),
    path('view-bill/<int:transaction_id>/', view_bill, name='view_bill'),
    path('all-orders/', all_orders, name='all_orders'),
    path('contact-us/', contact_us_submit, name='contact_us'),
    path('change-password/', change_password, name='change_password'),
    path('privacy-policy/', privacy, name='privacy'),
    path('about-us/', about_us, name='about_us'),
    path('post-list/', post_list, name='post_list'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('add-posts/', add_posts, name='add_posts'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)