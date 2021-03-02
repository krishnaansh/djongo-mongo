from django.conf.urls import url, re_path
from django.urls import path, include
from rest_framework import routers
from odata.views import ProductViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter, Route, DynamicRoute



from rest_framework import renderers

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'get' : 'reterive',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'delete'

})
router = routers.DefaultRouter()
# router.register(r'products', ProductViewSet, r"tool")
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from .sitemaps import *

sitemaps_dict = {
    # 'category' : Category_Sitemap,
    'product' : Product_Sitemap,
    # 'order' : Order_Sitemap,
}



urlpatterns = [
    # path("api/", include(router.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict},
    name='django.contrib.sitemaps.views.sitemap'),
    path('products', product_list),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)