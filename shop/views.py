from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from .models import Category, Product, Cart, CartItem


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
    return cart



def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(
        is_active=True,
        stock__gt=0,
    ).select_related("category")

    query = request.GET.get("q", "").strip()
    if query:
        from django.db.models import Q

        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    cart_count = 0
    if request.session.session_key:
        cart = Cart.objects.filter(
            session_key=request.session.session_key
        ).first()
        if cart:
            cart_count = sum(
                item.quantity for item in cart.items.all()
            )

    return render(request, "index.html", {
        "categories": categories,
        "products": products,
        "cart_count": cart_count,
        "query": query,
    })



@require_POST
@transaction.atomic
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product.objects.select_for_update(),
        pk=product_id,
        is_active=True,
    )

    cart = get_or_create_cart(request)
    item = CartItem.objects.filter(
        cart=cart, product=product
    ).first()

    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("home")

    if item:
        if item.quantity >= product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("home")
        item.quantity += 1
        item.save(update_fields=["quantity"])
    else:
        CartItem.objects.create(
            cart=cart, product=product, quantity=1
        )

    messages.success(request, f"{product.name} added to cart.")
    return redirect("home")


def cart_detail(request):
    cart = None
    if request.session.session_key:
        cart = Cart.objects.filter(
            session_key=request.session.session_key
        ).first()

    items = cart.items.select_related(
        "product"
    ).all() if cart else []

    total = sum(item.subtotal for item in items)

    return render(request, "shop/cart.html", {
        "items": items,
        "total": total,
    })