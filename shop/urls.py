from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart"),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
]
