from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('confirmation/', views.confirmation, name = 'confirmation'),
    path('update_item/', views.updateItem, name = 'update_Item'),
    path('process_order/', views.processOrder, name = 'process_order'),
    # path('addUserInfoForm/',views.addUserInfoForm, name='addUserInfoForm'),
    path('registerUser/',views.registerUserpage, name='registerUserpage'),
    path('login/',views.LoginPage, name='LoginPage'),
    path('profile/',views.userProfile, name='Profile'),
    path('logout/',views.LogoutPage, name='LogoutPage'),
]
