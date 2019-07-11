from django.shortcuts import render, redirect
from . import models
from decimal import Decimal
from django.http import JsonResponse
# Create your views here.


# #     for cart icon
def get_cart_icon():
    return models.Cart_Icon.objects.get(pk=1)


# #     for dropdown
def get_all_categories():
    return models.Category.objects.all()


def get_all_products():
    return models.Product.objects.all()


# #     to get given cart
def get_cart(request):
    carts = models.Cart.objects.all()
    k = 0
    for i in carts:
        if request.user == i.user:
            k += 1
    if k == 1:
        cart = models.Cart.objects.get(user=request.user)
    else:
        cart = models.Cart.objects.create(user=request.user, cart_total_price=0.00)
    return cart


# #     to change cart amount and total_price
def set_cart(cart):
    cart_total_price = 0.00
    cart_total_amount = 0
    for i in cart.items.all():
        cart_total_price += float(i.item_total_price)
        cart_total_amount += i.amount
    cart.cart_total_price = cart_total_price
    cart.cart_total_amount = cart_total_amount
    cart.save()


def base(request):
    icon = get_cart_icon().image
    categories = get_all_categories()
    return render(request, 'commerce/base.html', {'categories': categories, 'icon': icon, 'cart': get_cart(request)})


def homepage(request):
    products = get_all_products()
    categories = get_all_categories()
    icon = get_cart_icon().image
    products_for_carousel = models.Product.objects.filter(to_carousel=True)
    args = {
            'products': products,
            'products_for_carousel': products_for_carousel,
            'categories': categories,
            'icon': icon,
            'cart': get_cart(request),
            }
    return render(request, 'commerce/home.html', args)


def category_view(request, slug):
    icon = get_cart_icon().image
    category = models.Category.objects.get(slug=slug)
    products = models.Product.objects.filter(category=category).order_by('pk')
    categories = get_all_categories()
    args = {
            'products': products,
            'categories': categories,
            'category': category,
            'icon': icon,
            'cart': get_cart(request),
            }
    return render(request, 'commerce/category_view.html', args)


def cart_view(request):
    icon = get_cart_icon().image
    categories = get_all_categories()
    cart = get_cart(request)
    args = {
        'items': cart.items.all(),
        'categories': categories,
        'icon': icon,
        'cart': cart,
    }
    return render(request, 'commerce/cart_view.html', args)


def search(request):
    icon = get_cart_icon().image
    categories = get_all_categories()
    products = []
    args = {}
    k = 0
    if 'q' in request.GET:
        query = request.GET['q']
        for i in get_all_products():
            if str(query).lower() in str(i.name).lower():
                k += 1
                products.append(i)
        if k != 0:
            args = {
                'products': products,
                'name': query,
                'categories': categories,
                'icon': icon,
                'query': query,
                'count': len(products),
                'cart': get_cart(request),
            }
        else:
            args = {
                'products': '',
                'name': query,
                'categories': categories,
                'icon': icon,
                'cart': get_cart(request),
            }
    return render(request, 'commerce/search_done.html', args)


def add_to_cart(request):
    cart = get_cart(request)
    cart.add_to_cart(request.GET.get('product_slug'))
    set_cart(cart)
    return JsonResponse({
        'cart_total': cart.items.count(),
        'cart_total_price': cart.cart_total_price,
        'total_amount': cart.cart_total_amount,
    })


def remove_from_cart(request):
    cart = get_cart(request)
    cart.remove_from_cart(request.GET.get('product_slug'))
    set_cart(cart)
    return JsonResponse({
                'cart_total': cart.items.count(),
                'cart_total_price': cart.cart_total_price,
                'total_amount': cart.cart_total_amount,
            })


def product_details(request, slug):
    product = models.Product.objects.get(slug=slug)
    args = {
        'product': product,
        'categories': get_all_categories(),
        'icon': get_cart_icon().image,
        'cart': get_cart(request),
    }
    return render(request, 'commerce/product_details.html', args)


def change_item_amount(request):
    item_amount = request.GET.get('amount')
    item_id = request.GET.get('item_id')
    item = models.CartItem.objects.get(id=item_id)
    item.amount = item_amount
    item.item_total_price = int(item_amount) * Decimal(item.product.price)
    item.save()
    cart = get_cart(request)
    set_cart(cart)
    return JsonResponse({'cart_total': cart.items.count(),
                         'item_total': item.item_total_price,
                         'cart_total_price': cart.cart_total_price,
                         'total_amount': cart.cart_total_amount})