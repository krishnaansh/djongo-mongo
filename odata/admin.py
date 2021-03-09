from string import Template
from django.contrib import admin
from odata.models import *
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django import forms
from django.utils.safestring import mark_safe
from django.forms import ImageField
from import_export.admin import ImportExportModelAdmin
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


admin.site.register(Customer)
from django.contrib import admin
from django.utils.safestring import mark_safe

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
    inlines= [ProductModelInline ]
    list_display = ('product_name','current_order','quantity_per_unit','unit_price', 'msrp','image_tag','created_at', 'updated_at')
    form = ProductModelForm

    # def render_change_form(self, request, context, *args, **kwargs):
    #     #here we define a custom template
    #     self.change_form_template = 'contapp/change_form_template.html'
    #     extra = {
    #         "help_text" : "To delete multiple image select the checkbox and do save"
    #     }
    #     context.update(extra)
    #     return super(ProductAdmin, self).render_change_form(request, context, *args, **kwargs)

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

# admin.site.register(Suppliers)
admin.site.register(Category)
admin.site.register(Shipper)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderDetail)
# UnRegister your model.
# admin.site.unregister(User)
# admin.site.unregister(Group)