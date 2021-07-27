from rest_framework import viewsets
from rest_framework.response import Response

from odata.models import Product, Customer, Categories, ProductVariant, ProductImage, NewsletterSubscription
from odata.serializers import (ProductSerializers, CustomerSerializers, CategorySerializers,
                               ProductImageSerializers, ProductVariantSerializers, NewsLetterSerializers)

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers



class ProductViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class ProductVariantViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializers


class NewsLetterViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsLetterSerializers
class CustomerViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    """ This viewset is used for crud operations"""

    queryset = Categories.objects.all()
    serializer_class = CategorySerializers
