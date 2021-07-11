from django.contrib.sitemaps import Sitemap
# from django.core.urlresolvers import reverse
from django.shortcuts import reverse
#
from .models import Categories, Product, Customer

# class Static_Sitemap(Sitemap):

#     priority = 1.0
#     changefreq = 'daily'


#     def items(self):
#         return ['about_view', 'contact_view']

#     def location(self, item):
#         return reverse(item)


class Category_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Categories.objects.all()

    

    def lastmod(self, obj): 
        return obj.updated_at

class Product_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    

    def lastmod(self, obj): 
        return obj.updated_at

class Customer_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Customer.objects.all()

    

    def lastmod(self, obj): 
        return obj.updated_at
