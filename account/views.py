from django.shortcuts import render, redirect
from . import forms
from . import models
from commerce import views as commerce_views
# Create your views here.


def register(request):
    cart = commerce_views.get_cart(request)
    categories = commerce_views.get_all_categories()
    icon = commerce_views.get_cart_icon()
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/account/login/')
        else:
            return redirect('/account/register/')
    else:
        form = forms.RegistrationForm()
        args = {'form': form, 'categories': categories, 'icon': icon, 'cart': cart}
        return render(request, 'account/register.html', args)


def profile_view(request):
    cart = commerce_views.get_cart(request)
    categories = commerce_views.get_all_categories()
    icon = commerce_views.get_cart_icon()
    args = {'user': request.user, 'categories': categories, 'icon': icon, 'cart': cart}
    return render(request, 'account/profile_view.html', args)


def have_to_login(request):
    cart = commerce_views.get_cart(request)
    categories = commerce_views.get_all_categories()
    icon = commerce_views.get_cart_icon()
    args = {'categories': categories, 'icon': icon, 'cart': cart}
    return render(request, 'account/have_to_login.html', args)


def profile_edit(request):
    cart = commerce_views.get_cart(request)
    categories = commerce_views.get_all_categories()
    icon = commerce_views.get_cart_icon()
    profile = models.UserProfile.objects.get_or_create(user=request.user)
    profile = models.UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = forms.UserEdit(request.POST, instance=request.user)
        form1 = forms.ProfileEdit(request.POST, instance=profile)

        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('/account/profile/')
        else:
            return redirect('/account/profile/edit/')
    else:
        form = forms.UserEdit(instance=request.user)
        form1 = forms.ProfileEdit(instance=profile)
        args = {'form': form, 'form1': form1, 'categories': categories, 'icon': icon, 'cart': cart}
        return render(request, 'account/profile_edit.html', args)