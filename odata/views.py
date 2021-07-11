from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_sitemaps import Sitemap
from rest_framework import viewsets
from rest_framework.response import Response

from odata.models import Product, Customer, Categories
from odata.serializers import ProductSerializers, CustomerSerializers, CategorySerializers

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
    
    queryset = Categories.objects.all()
    serializer_class = CategorySerializers    

