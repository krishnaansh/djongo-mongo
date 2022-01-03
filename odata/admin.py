from bson import ObjectId
from django import forms
from django.contrib import admin
from django.contrib.admin import helpers, widgets
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group, User

from import_export.admin import ImportExportModelAdmin

from odata.models import *
from odata.exportimport.productresources import ProductResources


import logging
log = logging.getLogger(__name__)
# convert the errors to text
from django.utils.encoding import force_text

# admin.site.disable_action('delete_selected')
# Register your models here.
categories = Categories.objects.all()
categories_choice = [('', '-----')]
if categories:
    categories_choice = [(x._id, x.category_name) for x in categories]

products = Product.objects.all()
products_choice = [('', '-----')]
if products:
    products_choice = [(x._id, x.product_name) for x in products]
    
class ProductModelForm(forms.ModelForm):
    category = forms.ChoiceField(choices=categories_choice)
    class Meta:
        model = Product
        fields = '__all__'
    
    def is_valid(self):
        log.info(force_text(self.errors))
        return super(ProductModelForm, self).is_valid()
    # def clean(self):
    #     # Validation goes here :)
    #     raise forms.ValidationError("TEST EXCEPTION!")    


class ProductModelInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'
    
    def is_valid(self):
        log.info(force_text(self.errors))
        return super(ProductModelForm, self).is_valid()


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    icon_name = 'store'
    resource_class = ProductResources
    inlines= [ProductModelInline]
    list_display = ('product_name','quantity','price', 'msrp','image_tag','created_at', 'updated_at')
    form = ProductModelForm
    list_per_page = 15
    actions = ['make_deleted']
    
    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = Product.objects.get(pk=i)
            pro_img = ProductImage.objects.filter(product=query).delete()
            query.delete()

    make_deleted.short_description ='Delete selected product'

    class Media:
        js = ('js/tinmc.js',)
        
    def image_tag(self,obj):
        image_str = ''
        if obj.picture:
            image_str = '<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.picture)
        product_images = ProductImage.objects.filter(product=obj)        
        if product_images:
            for pro_img in product_images:
                if pro_img.image:
                    try:
                        image_str += ' <img src="{0}" style="width: 45px; height:45px;" />'.format(pro_img.image)
                    except :
                        pass
        return format_html(image_str)
        
    def save_model(self, request, obj, form, change):
        super(ProductAdmin, self).save_model(request, obj, form, change)

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    icon_name = 'device_hub'
    search_fields = ('category_name', )
    list_per_page = 15
    actions = ['make_deleted']
    
    
    def get_object(self, request, object_id, from_field=None):
        """
        Return an instance matching the field and value provided, the primary
        key is used if no field is provided. Return ``None`` if no match is
        found or the object_id fails validation.
        """
        
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: ObjectId( object_id)})
        except (model.DoesNotExist,ValueError):
            return None

    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = Categories.objects.get(pk=i)
            query.delete()

    make_deleted.short_description ='Delete selected category'
    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        return form


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_name = 'person'
    exclude = ('user',)
    list_per_page = 15
    actions = ['make_deleted']
    def save_model(self, request, obj, form, change):
        import random, string
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create(username=x)
        obj.user = user
        super().save_model(request, obj, form, change)
    
    
    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = Customer.objects.get(pk=i)
            query.delete()

    make_deleted.short_description ='Delete selected customer'
    

class ProductVariantForm(forms.ModelForm):
    parent_product = forms.ChoiceField(choices=products_choice)
    class Meta:
        model = ProductVariant
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('parent_product'):
            product = Product.objects.get(pk=ObjectId(cleaned_data['parent_product']))
            cleaned_data['parent_product'] = product

        return cleaned_data


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    icon_name = 'child_friendly'
    list_per_page = 15
    search_fields = ('parent_product__title',)
    form = ProductVariantForm
    actions = ['make_deleted']
    
    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = ProductVariant.objects.get(pk=i)
            query.delete()

    make_deleted.short_description ='Delete selected product variant'



@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    icon_name = 'picture_in_picture'
    list_per_page = 15
    
    actions = ['make_deleted']
    
    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = NewsletterSubscription.objects.get(pk=i)
            query.delete()

    make_deleted.short_description ='Delete selected NewsLetter'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    icon_name = 'payment'
    actions = ['make_deleted']
    
    def make_deleted(modeladmin, request, queryset):
        obj_ids = [ObjectId(i) for i in request.POST.getlist('_selected_action')]
        for i in obj_ids:
            query = Payment.objects.get(pk=i)
            query.delete()

    make_deleted.short_description ='Delete selected payment'
    
@admin.register(UserForgotPassword)
class UserForgotPasswordAdmin(admin.ModelAdmin):
    icon_name = 'password'
# UnRegister your model.
# admin.site.unregister(User)
# admin.site.unregister(Group)
