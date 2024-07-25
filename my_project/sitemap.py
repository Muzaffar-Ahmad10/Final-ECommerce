from django.contrib.sitemaps import Sitemap
from mainapp.models import Post
from products.models import Product

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.created_on

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at