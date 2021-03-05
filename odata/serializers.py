from django.contrib.auth.models import User
from rest_framework import serializers
from odata.models import Product, Customer, Category, Shipper, Order, OrderDetail

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class CustomerSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    class Meta:
        model = Customer
        fields = ['user', 'username', 'email', 'first_name', 'last_name', 'customer_class', 'room', 'building', 'address1', 'address2', 'city', 'state', 'postal_code',
                 'country', 'phone', 'voice_mail', 'password', 'credit_card', 'credit_card_type_id', 'card_exp_month', 'card_exp_month', 'billing_address', 'billing_city',
                 'billing_region', 'billing_postal_code', 'billing_country', 'ship_address', 'ship_city', 'ship_region', 'ship_postal_code', 'ship_country', 'date_entered', 
                 ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        # instance = Customer(**validated_data)
        user = User.objects.create(first_name=validated_data['first_name'], last_name=validated_data['last_name'], email=email, username=username)
        # instance.user = user
        instance = Customer.objects.filter(user=user).update(**validated_data)
        return Customer.objects.get(user=user)

    def validate(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        if User.objects.filter(email=email):
            raise serializers.ValidationError({"email" : "Email is already registered with us"})
                
        if User.objects.filter(username=username):
            raise serializers.ValidationError({"username" : "Username is already registered with us"})     

        # if    

        return validated_data
    
    def to_representation(self, instance):
        instance.username = instance.user.username
        instance.email = instance.user.email
        rep =  super(CustomerSerializers, self).to_representation(instance)
        rep['username'] = instance.user.username
        rep['email'] = instance.user.email
        return rep
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShipperSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shipper
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'