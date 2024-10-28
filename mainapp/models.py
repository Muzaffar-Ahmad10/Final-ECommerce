from django.db import models
from django.contrib.auth.models import User
from cart.models import SoldProduct
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField(default="", blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=[(0, "Draft"), (1, "Published")], default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    created_at = models.DateTimeField(auto_now_add=True)
    sold_products = models.ManyToManyField(SoldProduct, through='TransactionProduct')

    def __str__(self):
        return f'Transaction #{self.id} - User: {self.user.username}, Total: {self.total_bill}, Status: {self.payment_status}'


class TransactionProduct(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    sold_product = models.ForeignKey(SoldProduct, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Transaction #{self.transaction.id} - Sold Product: {self.sold_product.product.name}, Quantity: {self.sold_product.quantity}'


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email