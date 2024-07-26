from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.models import  TransactionProduct, Transaction
from products.models import Product
from cart.models import CartItem, SoldProduct
import stripe
from django.conf import settings
from random import sample
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="/login/")
@csrf_exempt
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
@csrf_exempt
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if cart_items.exists():
        return render(request, 'mainapp/cart.html', {
            'cart_items': cart_items,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    else:
        messages.info(request, "Your cart is empty.")
        return render(request, 'mainapp/cart.html', {
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
        return render(request, 'mainapp/checkout.html', {
            'cart_items': cart_items,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })


@login_required(login_url="/login/")
@csrf_exempt
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