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

RANKING = (
    ('promoted', 'Promoted'),
    ('best_seller', 'Best Seller'),
)
class Categories(models.Model):    
    objects = models.DjongoManager()
    id = models.AutoField(primary_key=True)    
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length=100,null=True,blank=True)  
    category_name_de = models.CharField(max_length=100,null=True,blank=True)  
    picture = models.ImageField(null=True,blank=True, upload_to="images")
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = 'odata_category'
    


class Customer(models.Model):
    """This model is used for customer"""    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)    
    address1 = models.CharField(max_length=100,null=True,blank=True)
    address2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    password = models.CharField(max_length=100)
    salutation = models.CharField(max_length=100,null=True,blank=True)
    credit_card = models.CharField(max_length=15)
    credit_card_type_id = models.CharField(max_length=100)
    mm_yy = models.CharField(max_length=7, null=True, blank=True)
    billing_address = models.CharField(max_length=250)
    billing_city = models.CharField(max_length=100)    
    billing_postal_code = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    ship_address = models.CharField(max_length=250)
    ship_city = models.CharField(max_length=250)
    ship_region = models.CharField(max_length=250)
    ship_postal_code = models.CharField(max_length=100)
    ship_country = models.CharField(max_length=100)
    marketing_code = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    medium = models.CharField(max_length=100, null=True, blank=True)
    gcustid = models.CharField(max_length=512, null=True, blank=True)
    gclid = models.CharField(max_length=1024, null=True, blank=True)
    fbclid = models.CharField(max_length=1024, null=True, blank=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    terms_condition = models.BooleanField(default=True)
    data_privacy = models.BooleanField(default=True)
    guest_login = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name+' '+self.last_name
        elif self.first_name is not None:
            return self.first_name
        else:
            return ''

# @receiver(post_save, sender=User)
# def create_user_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_customer(sender, instance, **kwargs):
#     instance.customer.save()
    

    
class Product(models.Model):
    """This models is used for Products Details."""        
    id = models.AutoField(primary_key=True)        
    vendor_product_id = models.CharField(max_length=50,null=True,blank=True)
    product_name = models.CharField(max_length=100)    
    category_id = models.ForeignKey(Categories, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.FloatField()
    msrp = models.CharField(max_length=100)
    ean = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=1024)
    title_de = models.CharField(max_length=1024, blank=True, null=True)
    available_size = models.CharField(max_length=3,choices=Available_Size)
    available_color = models.CharField(max_length=3,choices=Available_Color)
    size = models.CharField(max_length=100,null=True,blank=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    discount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Discount %")
    product_availble = models.BooleanField(default=False)        
    picture = models.ImageField(null=True,blank=True, upload_to="images")
    ranking = models.CharField(max_length=15,choices=RANKING)
    description = models.TextField(max_length=200)
    description_de = models.TextField(max_length=200, blank=True, null=True)
    product_highlight = models.TextField(max_length=200)
    product_highlight_de = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products", args=[str(self.id)])
    
    
class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_order = models.IntegerField()
    image = models.ImageField(null=True,blank=True, upload_to="images")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    

class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    parent_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    
# class Shipper(models.Model):
#     id = models.AutoField(primary_key=True)
#     company_name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

# class Order(models.Model):    
#     id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     order_number = models.CharField(max_length=100,null=True,blank=True)
#     payment_id = models.CharField(max_length=50,null=True,blank=True)
#     order_date = models.DateTimeField(auto_now_add=True)
#     ship_date = models.DateTimeField(default='')
#     required_date = models.DateField()    
#     freight = models.CharField(max_length=100,null=True,blank=True)
#     sale_tax = models.CharField(max_length=100,null=True,blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     transaction_status = models.CharField(max_length=1,choices=Trasaction_status)
#     error_lock = models.CharField(max_length=100,null=True,blank=True)
#     error_msg = models.CharField(max_length=100,null=True,blank=True)
#     fullfiled = models.BooleanField(default=False)
#     deleted = models.BooleanField(default=False)
#     paid = models.BooleanField(default=False)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

#     def __str__(self):
#         return self.order_number

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.CharField(max_length=100)
    invoice = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    date_of_payment = models.DateField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    
# class OrderDetail(models.Model):
#     id = models.AutoField(primary_key=True)
#     order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False, blank=False)
#     order_number = models.CharField(max_length=100,null=True,blank=True)
#     payment_id = models.CharField(max_length=50,null=True,blank=True)
#     price = models.DecimalField(max_digits=19, decimal_places=2)
#     quatity = models.IntegerField()
#     discount = models.DecimalField(decimal_places=2, max_digits=10)
#     total = models.IntegerField()
#     idsku = models.CharField(max_length=100,null=True,blank=True)
#     size = models.CharField(max_length=3,choices=Available_Size)
#     color = models.CharField(max_length=3,choices=Available_Color)
#     fullfield = models.BooleanField(default=False)
#     bill_date = models.DateField(default='')    
#     created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
#     def __str__(self):
#         return self.order.order_number
    
class NewsletterSubscription(models.Model):
    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=3)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    data_acceptance = models.BooleanField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)