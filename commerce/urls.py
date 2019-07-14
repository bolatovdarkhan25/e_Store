from django.urls import path
from . import views as commerce_views

urlpatterns = [
    path('base/', commerce_views.base, name='base'),
    path('', commerce_views.homepage, name='homepage'),
    path('category/<slug>/', commerce_views.category_view, name='category_view'),
    path('cart/', commerce_views.cart_view, name='cart_view'),
    path('search/', commerce_views.search, name='search'),
    path('cart/add_to_cart/', commerce_views.add_to_cart, name='add_to_cart'),
    path('cart/remove_from_cart/', commerce_views.remove_from_cart, name='remove_from_cart'),
    path('cart/change_item_amount/', commerce_views.change_item_amount, name='change_item_amount'),
    path('product/<slug>/', commerce_views.product_details, name='product_details'),
    path('order/formalization/', commerce_views.order, name='order'),
    path('orders/', commerce_views.show_my_orders, name='orders_list'),
    path('order/<pk>/view/', commerce_views.show_particular_order, name='show_order')
]