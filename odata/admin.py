from django import forms
from django.contrib import admin
from django.forms import ImageField
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

class ProductVariantAdmin(admin.StackedInline):
    model = ProductVariant
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
    resource_class = ProductResources
    inlines= [ProductModelInline, ProductVariantAdmin ]
    list_display = ('product_name','quantity','price', 'msrp','image_tag','created_at', 'updated_at')
    form = ProductModelForm

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
                    image_str += ' <img src="{0}" style="width: 45px; height:45px;" />'.format(pro_img.image.url)
        return format_html(image_str)

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):

    search_fields = ('category_name', )   
    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        return form


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        import random, string
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create(username=x)
        obj.user = user
        super().save_model(request, obj, form, change)
    

admin.site.register(Payment)
admin.site.register(NewsletterSubscription)
# UnRegister your model.
# admin.site.unregister(User)
# admin.site.unregister(Group)