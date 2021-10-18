from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from odata.models import (
    Payment,
    Product,
    Customer,
    Categories,
    ProductVariant,
    ProductImage,
    NewsletterSubscription,
)
from odata.serializers.serializers import (
    ProductSerializers,
    CustomerSerializers,
    CategorySerializers,
    PaymentSerializers,
    ProductImageSerializers,
    ProductVariantSerializers,
    NewsLetterSerializers,
)

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    
    def get_serializer_context(self):
        context = super(ProductViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class ProductImageViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class ProductVariantViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializers


class NewsLetterViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsLetterSerializers
    permission_classes = [IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """This viewset is used for crud operations"""

    queryset = Categories.objects.all()
    serializer_class = CategorySerializers


class PaymentViewset(viewsets.ModelViewSet):
    """
    This viewset is used for crud operation
    """
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializers
    permission_classes = [IsAuthenticated]
