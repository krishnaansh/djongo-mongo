from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_sitemaps import Sitemap
from rest_framework import viewsets
from rest_framework.response import Response

from odata.models import Product, Customer, Category, Shipper, Order, OrderDetail
from odata.serializers import ProductSerializers, CustomerSerializers, CategorySerializers, ShipperSerializers
from odata.serializers import OrderSerializers, OrderDetailSerializers

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializers    

class CustomerViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers    

class CategoryViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializers    

class ShipperViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializers    

class OrderViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializers    

class OrderDetailViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""
    
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializers            
# from app.pages.sitemaps import PagesSitemap

# def sitemap(request):
#     sitemap = Sitemap(
#         # All URLs are passed through build_absolute_uri.
#         build_absolute_uri=request.build_absolute_uri,
#     )

#     # URLs can be added one-by-one. The only required argument
#     # is the URL. All other arguments are keyword-only arguments.
#     for p in Page.objects.active():
#         url = p.get_absolute_url()
#         sitemap.add(
#             url,
#             changefreq='weekly',
#             priority=0.5,
#             lastmod=p.modification_date,
#             alternates={
#                 code: urljoin(domain, url)
#                 for code, domain in PAGE_DOMAINS[p.language].items()
#             },
#         )

#     # Adding conventional Django sitemaps is supported. The
#     # request argument is necessary because Django's sitemaps
#     # depend on django.contrib.sites, resp. RequestSite.
#     sitemap.add_django_sitemap(PagesSitemap, request=request)

#     # You could get the serialized XML...
#     # ... = sitemap.serialize([pretty_print=False])
#     # ... or use the ``response`` helper to return a
#     # ready-made ``HttpResponse``:
#     return sitemap.response(
#         # pretty_print is False by default
#         pretty_print=settings.DEBUG,
#     )