from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Transaction, ContactUs, Post
from products.models import Product, ProductImage
import stripe
from django.conf import settings
from random import sample
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def index(request):
    products = Product.objects.all()
    product_images = {product.id: ProductImage.objects.filter(product=product).first() for product in products}
    if request.method == 'POST':
        if "index-contact-form" in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            if name and email is not None:
                ContactUs.objects.create(name=name, email=email, message=message)
                messages.success(request, 'Your message has been sent successfully. We will get back to you soon.')
            else:
                messages.error(request, "Name or Email missing!")
    messages.success(request, 'Welcome to our IshopPC!')
    context = {
        'products': products,
        'product_images': product_images,
    }
    return render(request, 'mainapp/index.html', context)


@superuser_required
def dashboard(request):
    messages.success(request, 'Welcome to your dashboard!')
    return render(request, 'mainapp/dashboard.html')


@login_required(login_url="/login/")
def hot_products(request):
    products = sample(list(Product.objects.all()), min(6, Product.objects.count()))
    context = {
        'products': products,
    }
    return render(request, 'mainapp/hot_products.html', context)

@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            if password1 != password2:
                raise ValueError('Passwords do not match')
            
            if User.objects.filter(username=username).exists():
                raise ValueError('Username already exists')
            
            if User.objects.filter(email=email).exists():
                raise ValueError('Email already exists')
            
            user = User.objects.create(username=username, email=email, password=make_password(password1))
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')

        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again.')

    return render(request, 'mainapp/signup.html')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome back.')

            if user.is_superuser:
                return redirect('dashboard') 
            else:
                return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'mainapp/login.html')



@login_required(login_url="/login/")
def my_orders(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mainapp/my_orders.html', {'transactions': transactions})


@superuser_required
def all_orders(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'mainapp/all_orders.html', {'transactions': transactions})


@login_required(login_url="/login/")
def view_bill(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'mainapp/view_bill.html', {'transaction': transaction})

@csrf_exempt
def contact_us_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email is not None:
            ContactUs.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully. We will get back to you soon.')
            return redirect('contact_us')
        else:
            messages.error(request, "Name or Email missing!")
            return redirect('contact_us')

    return render(request, 'mainapp/contact_us.html')


@login_required(login_url="/login/")
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mainapp/change_password.html', {'form': form})


def privacy(request):
    return render(request, 'mainapp/privacy.html')


def about_us(request):
    return render(request, 'mainapp/about_us.html')

def post_list(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    return render(request, 'mainapp/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    return render(request, 'mainapp/post_detail.html', {'post': post})


@superuser_required
@csrf_exempt
def add_posts(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            messages.success(request, "Post Deleted Successfully")
            post.save()
            return redirect('add_posts')
    else:
        messages.success(request, "Something went wrong")
        form = PostForm()
    
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        'form': form,
    }
    return render(request, 'mainapp/add_posts.html', context)

@superuser_required
@csrf_exempt
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        messages.success(request, "Post Deleted Successfully")
        post.delete()
    return redirect('add_posts')

def custom_page_not_found_view(request, exception):
    return render(request, 'mainapp/404.html', status=404)