from django.conf.urls import url, re_path
from django.urls import path, include

from rest_framework import routers
from rest_framework.routers import SimpleRouter, DefaultRouter, Route, DynamicRoute
from odata.views import ProductViewSet, CustomerViewSet, CategoryViewSet, ShipperViewSet
from odata.views import OrderViewSet, OrderDetailViewSet



from rest_framework import renderers

viewset_dict = {
    'get': 'list',
    'post': 'create',
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'

}

class CustomSimpleRouter(SimpleRouter):
    routes = [
        # List route
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "list",
                "post": "create",
                "put": "bulk_update",
                # "delete": "destroy",
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # Detail route
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=False,
            initkwargs={"suffix": "Instance"},
        ),
    ]

router = CustomSimpleRouter()
product_list = ProductViewSet.as_view(viewset_dict)
customer_list = CustomerViewSet.as_view(viewset_dict)
category_list = CategoryViewSet.as_view(viewset_dict)
shipper_list = ShipperViewSet.as_view(viewset_dict)
order_list = OrderViewSet.as_view(viewset_dict)
orderdetail_list = OrderDetailViewSet.as_view(viewset_dict)


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


router.register(r"products", ProductViewSet),
router.register(r"customers", CustomerViewSet),
router.register(r"category", CategoryViewSet),
router.register(r"shipper", ShipperViewSet),
router.register(r"orders", OrderViewSet),
router.register(r"orderdetails", OrderDetailViewSet),
urlpatterns = [
    # path("api/", include(router.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict},
    name='django.contrib.sitemaps.views.sitemap'),
    path("", include(router.urls)),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)