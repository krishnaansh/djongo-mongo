from .sitemaps import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from rest_framework import routers
from rest_framework.routers import SimpleRouter, Route
from odata.views import (
    ProductViewSet,
    CustomerViewSet,
    CategoryViewSet,
    PaymentViewset,    
    NewsLetterViewSet,
)


viewset_dict = {
    "get": "list",
    "post": "create",
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
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


router = routers.DefaultRouter()
# router.register(r'products', ProductViewSet, r"tool")

sitemaps_dict = {
    # 'category' : Category_Sitemap,
    "product": Product_Sitemap,
    # 'order' : Order_Sitemap,
}


router.register(r"products", ProductViewSet),
router.register(r"payments", PaymentViewset),
# router.register(r"products/image", ProductImageViewSet),
# router.register(r"products/variant", ProductVariantViewSet),
router.register(r"newsletter", NewsLetterViewSet),
router.register(r"customers", CustomerViewSet),
router.register(r"category", CategoryViewSet),
urlpatterns = [
    # path("api/", include(router.urls)),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
