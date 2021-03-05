# from django.db import models
# 
# Create your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import reverse
from djongo import models

     
Available_Size = (
    ('S', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
  ('XL', 'extra large'),
)
Available_Color = (
    ('w','white'),
    ('b','black'),
    ('g','green'),
    ('y','yellow'),
)

Trasaction_status = (
    ('1', 'Done'),
    ('2', 'pending'),
    ('3', '--------'),
)

PAYMENT_MODE = (
    ('online', 'online'),
    ('offline', 'offline'),
)

class Category(models.Model):    
    objects = models.DjongoManager()
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(max_length=300,null=True,blank=True)
    picture = models.ImageField(null=True,blank=True, upload_to="images")
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.category_name


class Customer(models.Model):
    """This model is used for customer"""
    # customer_id = models.CharField(max_length=10,null=True,blank=True)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    customer_class = models.CharField(max_length=100,null=True,blank=True) # have doubt
    room = models.CharField(max_length=100,null=True,blank=True)
    building = models.CharField(max_length=100,null=True,blank=True)
    address1 = models.CharField(max_length=100,null=True,blank=True)
    address2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)    
    voice_mail = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100)
    credit_card = models.CharField(max_length=15)
    credit_card_type_id = models.CharField(max_length=100)
    card_exp_month = models.IntegerField()
    card_exp_year = models.IntegerField()
    billing_address = models.CharField(max_length=250)
    billing_city = models.CharField(max_length=100)
    billing_region = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    ship_address = models.CharField(max_length=250)
    ship_city = models.CharField(max_length=250)
    ship_region = models.CharField(max_length=250)
    ship_postal_code = models.CharField(max_length=100)
    ship_country = models.CharField(max_length=100)
    date_entered = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name+' '+self.last_name
        elif self.first_name is not None:
            return self.first_name
        else:
            return ''

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()

# class Suppliers(models.Model):
#     """
#     Supplier Model.
#     """
#     # supplier_id = models.CharField(max_length=100,null=True,blank=True)
#     company_name = models.CharField(max_length=100,null=True, blank=True)
#     contact_fname = models.CharField(max_length=100,null=True, blank=True)
#     contact_lname = models.CharField(max_length=100,null=True, blank=True)
#     contact_title = models.CharField(max_length=100,null=True, blank=True)
#     address1 = models.CharField(max_length=250,null=True, blank=True)
#     address2 = models.CharField(max_length=250,null=True, blank=True)
#     city = models.CharField(max_length=100,null=True, blank=True)
#     state = models.CharField(max_length=100,null=True, blank=True)
#     postal_code = models.IntegerField()
#     country = models.CharField(max_length=100,null=True, blank=True)
#     fax = models.CharField(max_length=100,null=True, blank=True)
#     email = models.EmailField()
#     url = models.URLField(max_length=200,null=True, blank=True)
#     payment_mode = models.CharField(max_length=10,choices=PAYMENT_MODE)
#     Discount_type = models.CharField(max_length=20,null=True, blank=True)
#     types_goods = models.CharField(max_length=100,null=True, blank=True)
#     notes = models.TextField(max_length=300,null=True, blank=True)
#     discount_avaiable = models.BooleanField(default=False)
#     current_order = models.CharField(max_length=100,null=True, blank=True) 
#     logo = models.ImageField(null=True,blank=True,default='')
#     # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')
#     size_url = models.CharField(max_length=100,null=True, blank=True)
    
#     def __str__(self):
#         return self.contact_fname+' '+self.contact_lname

# @receiver(post_save, sender=User)
# def create_user_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_customer(sender, instance, **kwargs):
#     instance.customer.save()
    
class Product(models.Model):
    """This models is used for Products Details."""
    # product_id = models.CharField(max_length=20)
    # objects = models.DjongoManager()
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100,null=True,blank=True)
    idsku = models.CharField(max_length=50,null=True,blank=True)
    vendor_product_id = models.CharField(max_length=50,null=True,blank=True)
    product_name = models.CharField(max_length=100)    
    # supplier_id = models.ForeignKey(Suppliers, on_delete=models.PROTECT) # It will foregin key of supplier
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    quantity_per_unit = models.IntegerField()
    unit_price = models.FloatField()
    msrp = models.CharField(max_length=100)
    available_size = models.CharField(max_length=3,choices=Available_Size)
    available_color = models.CharField(max_length=3,choices=Available_Color)
    size = models.CharField(max_length=100,null=True,blank=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    unit_weight = models.IntegerField()
    unit_in_stock = models.IntegerField()
    unit_or_order = models.IntegerField()
    reorder_level = models.CharField(max_length=100,null=True,blank=True)
    product_availble = models.BooleanField(default=False)
    discount_availble = models.CharField(max_length=100,null=True,blank=True)
    current_order = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(null=True,blank=True, upload_to="images")
    ranking = models.IntegerField()
    note = models.TextField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products", args=[str(self.id)])
    
    
class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True, upload_to="images")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    


    
class Shipper(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Order(models.Model):
    # order_id = models.CharField(max_length=50,null=True,blank=True)
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=50,null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    ship_date = models.DateTimeField(default='')
    required_date = models.DateField()
    # shipper_id = models.ForeignKey(Shipper, on_delete=models.CASCADE, db_column='shipper_id')
    freight = models.CharField(max_length=100,null=True,blank=True)
    sale_tax = models.CharField(max_length=100,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=1,choices=Trasaction_status)
    error_lock = models.CharField(max_length=100,null=True,blank=True)
    error_msg = models.CharField(max_length=100,null=True,blank=True)
    fullfiled = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.order_number

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    payment_type = models.CharField(max_length=10,choices=PAYMENT_MODE)
    allowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False, blank=False)
    order_number = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    quatity = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    total = models.IntegerField()
    idsku = models.CharField(max_length=100,null=True,blank=True)
    size = models.CharField(max_length=3,choices=Available_Size)
    color = models.CharField(max_length=3,choices=Available_Color)
    fullfield = models.BooleanField(default=False)
    bill_date = models.DateField(default='')    
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.order.order_number
    
    