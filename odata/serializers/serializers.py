from django.contrib.auth.models import User
from django.forms import fields
from rest_framework import request, serializers
from odata.models import (
    Product,
    Customer,
    Categories,
    ProductImage,
    ProductVariant,
    NewsletterSubscription,
    Payment,
)


class ProductImageSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = ProductImage
        fields = ("image_order", "image_url", "product")

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class ProductVariantSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        """
        Change in the response of api
        """
        rep = super(ProductSerializers, self).to_representation(instance)
        product_image = ProductImage.objects.filter(product=instance).order_by("-id")
        product_variant = ProductVariant.objects.filter(
            parent_product=instance
        ).order_by("-id")
        rep["product_image"] = ProductImageSerializers(
            product_image, many=True, context={"request": self.context.get("request")}
        ).data
        rep["product_variant"] = ProductVariantSerializers(
            product_variant, many=True
        ).data

        return rep


class NewsLetterSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = "__all__"


class CustomerSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    class Meta:
        model = Customer
        exclude = ("created_at", "updated_at")

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        # instance = Customer(**validated_data)
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=email,
            username=username,
        )
        # instance.user = user
        instance = Customer.objects.filter(user=user).update(**validated_data)
        return Customer.objects.get(user=user)

    def validate(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                {"email": "Email is already registered with us"}
            )

        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                {"username": "Username is already registered with us"}
            )

        # if

        return validated_data

    def to_representation(self, instance):
        instance.username = instance.user.username
        instance.email = instance.user.email
        rep = super(CustomerSerializers, self).to_representation(instance)
        rep["username"] = instance.user.username
        rep["email"] = instance.user.email
        return rep


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class PaymentSerializers(serializers.ModelSerializer):
    """
    Payment serializer
    """

    class Meta:
        """Paymet meta class"""

        model = Payment
        fields = "__all__"
