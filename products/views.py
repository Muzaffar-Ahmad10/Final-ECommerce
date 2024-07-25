from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.forms import modelformset_factory
from mainapp.forms import ProductForm, ProductImageForm
from mainapp.models import  TransactionProduct, Transaction, ContactUs
from products.models import Product, ProductImage
from cart.models import CartItem, SoldProduct
import stripe
from django.conf import settings
from random import sample
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from mainapp.decorators import superuser_required
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    return render(request, 'mainapp/add_product.html', {
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
    return render(request, 'mainapp/inventory.html', context)


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
    return render(request, 'mainapp/inventory.html', context)


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
def single_product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        images = product.images.all()

        context = {
            'product': product,
            'images': images,
        }
        return render(request, 'mainapp/single_product.html', context)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return render(request, 'mainapp/single_product.html')