from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from shop.api import api
from shop.views import add_to_cart, cart_view, create_order, index, products_list

urlpatterns = [
    path("", index),
    path("products", products_list),
    path("cart", cart_view),
    path("cart/add/<int:product_id>", add_to_cart),
    path("order", create_order),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
