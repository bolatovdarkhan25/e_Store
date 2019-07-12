from django.urls import path
from . import views as account_views
from django.contrib.auth.views import LogoutView, LoginView
urlpatterns = [
    path('profile/', account_views.profile_view, name='profile_view'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='commerce/home.html'), name='logout'),
    path('register/', account_views.register, name='register'),
    path('have-to-login/', account_views.have_to_login, name='have_to_login'),
    path('profile-edit/', account_views.profile_edit, name='profile_edit'),
]