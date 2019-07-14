from django.shortcuts import render, redirect
from . import models
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.models import User
from . import forms
from account import forms as account_forms
from account import models as account_models
# Create your views here.


# #     for cart icon
def get_cart_icon():
    return models.Cart_Icon.objects.get(pk=1).image


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
    icon = get_cart_icon()
    categories = get_all_categories()
    return render(request, 'commerce/base.html', {'categories': categories, 'icon': icon, 'cart': get_cart(request),
                                                  'user': request.user})


def homepage(request):
    products = get_all_products()
    categories = get_all_categories()
    icon = get_cart_icon()
    products_for_carousel = models.Product.objects.filter(to_carousel=True)
    if request.user not in User.objects.all():
        args = {
                'products': products,
                'products_for_carousel': products_for_carousel,
                'categories': categories,
                'user': request.user,
                }
    else:
        args = {
            'products': products,
            'products_for_carousel': products_for_carousel,
            'categories': categories,
            'icon': icon,
            'cart': get_cart(request),
            'user': request.user,
        }
    return render(request, 'commerce/home.html', args)


def category_view(request, slug):
    icon = get_cart_icon()
    category = models.Category.objects.get(slug=slug)
    products = models.Product.objects.filter(category=category).order_by('pk')
    categories = get_all_categories()
    if request.user not in User.objects.all():
        args = {
                'products': products,
                'categories': categories,
                'category': category,
                'user': request.user,
                }
    else:
        args = {
            'products': products,
            'categories': categories,
            'category': category,
            'icon': icon,
            'cart': get_cart(request),
            'user': request.user,
        }
    return render(request, 'commerce/category_view.html', args)


def cart_view(request):
    icon = get_cart_icon()
    categories = get_all_categories()
    args = {
        'items': get_cart(request).items.all(),
        'categories': categories,
        'icon': icon,
        'cart': get_cart(request),
        'user': request.user,
    }
    return render(request, 'commerce/cart_view.html', args)


def search(request):
    icon = get_cart_icon()
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
            if request.user not in User.objects.all():
                args = {
                    'products': products,
                    'name': query,
                    'categories': categories,
                    'query': query,
                    'count': len(products),
                    'user': request.user,
                }
            else:
                args = {
                    'products': products,
                    'name': query,
                    'categories': categories,
                    'icon': icon,
                    'query': query,
                    'count': len(products),
                    'cart': get_cart(request),
                    'user': request.user,
                }
        else:
            if request.user not in User.objects.all():
                args = {
                    'products': '',
                    'name': query,
                    'categories': categories,
                    'user': request.user,
                }
            else:
                args = {
                    'products': '',
                    'name': query,
                    'categories': categories,
                    'icon': icon,
                    'cart': get_cart(request),
                    'user': request.user,
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
    if request.user not in User.objects.all():
        args = {
            'product': product,
            'categories': get_all_categories(),
            'user': request.user,
        }
    else:
        args = {
            'product': product,
            'categories': get_all_categories(),
            'icon': get_cart_icon(),
            'cart': get_cart(request),
            'user': request.user,
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


def order(request):
    profile = account_models.UserProfile.objects.get_or_create(user=request.user)
    profile = account_models.UserProfile.objects.get(user=request.user)
    cart = get_cart(request)
    if request.method == "POST":
        order_form = forms.OrderForm(request.POST)
        user_form = account_forms.UserEdit(request.POST, instance=request.user)
        profile_form = account_forms.ProfileEdit(request.POST, instance=profile)

        if order_form.is_valid() and user_form.is_valid() and profile_form.is_valid():
            new_order = models.Order()
            new_order.user = request.user
            for i in range(len(cart.items.all())):
                if i == 0:
                    new_order.items.append('1) ' + cart.items.all()[i].product.name +
                                           '({} * {})'.format(cart.items.all()[i].amount,
                                                              cart.items.all()[i].product.price))
                else:
                    new_order.items.append('   {}) '.format(i + 1) + cart.items.all()[i].product.name +
                                           '({} * {})'.format(cart.items.all()[i].amount,
                                                         cart.items.all()[i].product.price))
            new_order.total_price = cart.cart_total_price
            new_order.buying_type = order_form.cleaned_data['buying_type']
            new_order.date = order_form.cleaned_data['date']
            new_order.address = order_form.cleaned_data['address']
            new_order.comments = order_form.cleaned_data['comments']
            new_order.save()
            user_form.save()
            profile_form.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        order_form = forms.OrderForm()
        user_form = account_forms.UserEdit(instance=request.user)
        profile_form = account_forms.ProfileEdit(instance=profile)

    args = {'order_form': order_form, 'user_form': user_form, 'profile_form': profile_form,
            'cart': get_cart(request), 'categories': get_all_categories(), 'icon': get_cart_icon()}
    return render(request, 'commerce/order.html', args)


def show_my_orders(request):
    orders = models.Order.objects.filter(user=request.user)
    args = {'orders': orders, 'cart': get_cart(request), 'categories': get_all_categories(), 'icon': get_cart_icon()}
    return render(request, 'commerce/orders_list.html', args)


def show_particular_order(request, pk):
    order = models.Order.objects.get(pk=pk)
    args = {'order': order, 'cart': get_cart(request), 'categories': get_all_categories(), 'icon': get_cart_icon()}
    return render(request, 'commerce/show_order.html', args)