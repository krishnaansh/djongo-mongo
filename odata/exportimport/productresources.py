from import_export import resources
from odata.models import Product

class ProductResources(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')