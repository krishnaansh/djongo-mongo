from django import forms
from django.contrib import admin
from django.forms import ImageField, fields
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group, User

from import_export.admin import ImportExportModelAdmin

from odata.models import *
from odata.exportimport.productresources import ProductResources

# Register your models here.
class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            img_html = mark_safe(f'<img src="{value.url}" width="50" height="50"/>')
            return f'{img_html}{input_html}'
        else:            
            return input_html
class ProductModelForm(forms.ModelForm):
    picture = ImageField(widget=PictureWidget)
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductModelInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'
    
    
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    icon_name = 'store'
    resource_class = ProductResources
    inlines= [ProductModelInline]
    list_display = ('product_name','quantity','price', 'msrp','image_tag','created_at', 'updated_at')
    form = ProductModelForm
    list_per_page = 15

    class Media:
        js = ('js/tinmc.js',)
        
    def image_tag(self,obj):
        image_str = ''
        if obj.picture:
            image_str = '<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.picture.url)
        product_images = ProductImage.objects.filter(product=obj)        
        if product_images:
            for pro_img in product_images:
                if pro_img.image:
                    try:
                        image_str += ' <img src="{0}" style="width: 45px; height:45px;" />'.format(pro_img.image.url)
                    except :
                        pass
        return format_html(image_str)

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    icon_name = 'device_hub'
    search_fields = ('category_name', )
    list_per_page = 15
    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        return form


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_name = 'person'
    exclude = ('user',)
    list_per_page = 15
    def save_model(self, request, obj, form, change):
        import random, string
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create(username=x)
        obj.user = user
        super().save_model(request, obj, form, change)
    

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    icon_name = 'child_friendly'
    list_per_page = 15
    search_fields = ('parent_product__title',)
@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    icon_name = 'picture_in_picture'
    list_per_page = 15

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    icon_name = 'payment'
# UnRegister your model.
# admin.site.unregister(User)
# admin.site.unregister(Group)
