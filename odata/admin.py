from django.contrib import admin
from odata.models import *
from django.contrib.auth.models import Group, User

# Register your models here.



admin.site.register(Customer)
# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):    
    list_display = ('product_name','current_order','quantity_per_unit','unit_price', 'msrp')
# admin.site.register(Suppliers)
admin.site.register(Category)
admin.site.register(Shipper)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderDetail)
# UnRegister your model.
# admin.site.unregister(User)
# admin.site.unregister(Group)