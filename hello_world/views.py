from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ProductForm, ProductImageForm
from .models import Product, ProductImage, CartItem, SoldProduct, TransactionProduct, Transaction, ContactUs
import stripe
from django.conf import settings
from random import sample
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    return render(request, 'hello_world/index.html', context)


@superuser_required
def dashboard(request):
    messages.success(request, 'Welcome to your dashboard!')
    return render(request, 'hello_world/dashboard.html')


@login_required(login_url="/login/")
def hot_products(request):
    products = sample(list(Product.objects.all()), min(6, Product.objects.count()))
    context = {
        'products': products,
    }
    return render(request, 'hello_world/hot_products.html', context)


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

    return render(request, 'hello_world/signup.html')


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

    return render(request, 'hello_world/login.html')



@superuser_required
@csrf_exempt
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()
            
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    alt_text = form.get('alt_text', '')
                    ProductImage(product=product, image=image, alt_text=alt_text).save()
            
            messages.success(request, "Product added successfully.")
            return redirect('add_product')
        else:
            messages.error(request, "There was an error with the form. Please correct the errors below.")
        
    else:
        product_form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    messages.success(request, "Welcome to Add Product!")

    return render(request, 'hello_world/add_product.html', {
        'product_form': product_form,
        'formset': formset,
    })


@superuser_required
@csrf_exempt
def inventory(request):
    products = Product.objects.all()
    ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1, can_delete=True)

    product_forms = []
    for product in products:
        if request.method == 'POST':
            product_form = ProductForm(request.POST, instance=product)
            formset = ProductImageFormSet(request.POST, request.FILES, queryset=product.images.all())
            if product_form.is_valid() and formset.is_valid():
                product_form.save()
                formset.save()
                messages.success(request, f"Changes saved for {product.name}.")
            else:
                messages.error(request, f"There was an error saving changes for {product.name}. Please correct the errors.")
        else:
            product_form = ProductForm(instance=product)
            formset = ProductImageFormSet(queryset=product.images.all())
        product_forms.append((product, product_form, formset))
    messages.success(request, "Welcome to Product Inventory")
    context = {
        'product_forms': product_forms,
    }
    return render(request, 'hello_world/inventory.html', context)


@superuser_required
@csrf_exempt
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1, can_delete=True)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=product.images.all())
        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            formset.save()
            messages.success(request, f"Changes saved for {product.name}.")
            return redirect('inventory')
        else:
            messages.error(request, f"There was an error saving changes for {product.name}. Please correct the errors.")
    else:
        product_form = ProductForm(instance=product)
        formset = ProductImageFormSet(queryset=product.images.all())
    
    context = {
        'product_form': product_form,
        'formset': formset,
        'product': product,
    }
    return render(request, 'hello_world/inventory.html', context)


@superuser_required
@csrf_exempt
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"{product_name} has been deleted successfully.")
        return redirect('inventory')
    else:
        messages.error(request, "Invalid request method. Please use POST to delete a product.")
        return redirect('inventory')
    
    
@login_required(login_url="/login/")
def single_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        images = product.images.all()

        context = {
            'product': product,
            'images': images,
        }
        return render(request, 'hello_world/single_product.html', context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return render(request, 'hello_world/single_product.html')



@login_required(login_url="/login/")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.stock > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        product.stock -= 1
        product.save()
        messages.success(request, f"{product.name} added to cart.")
    else:
        messages.error(request, "Sorry, this product is out of stock.")

    return redirect('cart')



@login_required(login_url="/login/")
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if cart_items.exists():
        return render(request, 'hello_world/cart.html', {
            'cart_items': cart_items,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    else:
        messages.info(request, "Your cart is empty.")
        return render(request, 'hello_world/cart.html', {
            'cart_items': cart_items,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    


@login_required(login_url="/login/")
@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip')
        stripe_token = request.POST.get('stripeToken')

        cart_items = CartItem.objects.filter(user=request.user)

        total_bill = sum(item.product.price * item.quantity for item in cart_items)

        try:
            charge = stripe.Charge.create(
                amount=int(total_bill * 100),
                currency='usd',
                description='Purchase from MyShop',
                source=stripe_token,
            )

            # Save sold products
            transaction = Transaction.objects.create(
                user=request.user,
                total_bill=total_bill,
                payment_status='Paid'
            )

            for item in cart_items:
                SoldProduct.objects.create(
                    user=request.user,
                    name=name,
                    address=address,
                    phone_number=phone,
                    zip_code=zip_code,
                    total_bill=item.product.price * item.quantity,
                    product=item.product,
                    quantity=item.quantity,
                )

                TransactionProduct.objects.create(
                    transaction=transaction,
                    sold_product=SoldProduct.objects.latest('id')
                )

            cart_items.delete()

            messages.success(request, "Thank you for your purchase! We hope you enjoy your goods soon.")
            return redirect('cart')
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {e.user_message}")
            return redirect('cart')
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'hello_world/checkout.html', {
            'cart_items': cart_items,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })


@login_required(login_url="/login/")
def clear_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if cart_items.exists():
        for item in cart_items:
            product = item.product
            product.stock += item.quantity
            product.save()
        cart_items.delete()
        messages.success(request, "Your cart has been cleared successfully.")
    else:
        messages.info(request, "Your cart is already empty.")
    
    return redirect('cart')


@login_required(login_url="/login/")
def my_orders(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'hello_world/my_orders.html', {'transactions': transactions})


@superuser_required
def all_orders(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'hello_world/all_orders.html', {'transactions': transactions})


@login_required(login_url="/login/")
def view_bill(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'hello_world/view_bill.html', {'transaction': transaction})

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

    return render(request, 'hello_world/contact_us.html')


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
    return render(request, 'hello_world/change_password.html', {'form': form})


def privacy(request):
    return render(request, 'hello_world/privacy.html')


def about_us(request):
    return render(request, 'hello_world/about_us.html')