from django.contrib.sitemaps import Sitemap
from mainapp.models import Post
from products.models import Product

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=1).order_by('created_on')  # Order by created_on

    def lastmod(self, obj):
        return obj.created_on

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Product.objects.all().order_by('updated_at')  # Order by updated_at

    def lastmod(self, obj):
        return obj.updated_at
