from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
from .forms import RegistrationForm, AccountAuthenticationForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from .filters import ChampionsFilter
from django.contrib import messages
import psycopg2
import hashlib
import os
from django.contrib.auth import get_user_model
UserModel = get_user_model()



def registerUserpage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')


            user_from_usermodel = UserModel._default_manager.get_by_natural_key(email)


            hash_save = Account.objects.get(id = user_from_usermodel.id )
            new_hash_val = hashlib.pbkdf2_hmac('sha256', raw_password.encode(), str.encode(user_from_usermodel.new_salt), 100000)
            hash_save.new_hash_value = new_hash_val.hex()

            hash_save.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
                )


            login(request, user_from_usermodel)  #log the user in
            return redirect('home')

    context ={'form':form}
    return render(request,'design/registerUser.html',context)

def LoginPage(request):

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = UserModel._default_manager.get_by_natural_key(email)


                hash_value_from_DB = user.new_hash_value
                hash_value = hashlib.pbkdf2_hmac('sha256', password.encode(), str.encode(user.new_salt), 100000) #output hash value
                hash_value = hash_value.hex()



                if hash_value == hash_value_from_DB:

                    login(request, user)
                    return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context={'form':form}
    return render(request, 'design/login.html', context)


def userProfile(request):
    customer = request.user.customer
    form = UserProfileForm(instance = customer)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Profile')

    context={'form':form}
    return render(request,'design/userProfile.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('home')

def home(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:

        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']


    champ = Champions.objects.all().order_by('name')
    myFilter = ChampionsFilter(request.GET, queryset=champ)
    if request.GET.get('price') == 'LTH':
        champ = Champions.objects.all().order_by('price','name')
        # myFilter = ChampionsFilter(request.GET, queryset=champ)
        # champ = myFilter.qs

    elif request.GET.get('price') == 'HTL':
        champ = Champions.objects.all().order_by('-price','name')
        # myFilter = ChampionsFilter(request.GET, queryset=champ)
        # champ = myFilter.qs

    myFilter = ChampionsFilter(request.GET, queryset=champ)
    champ = myFilter.qs

    context = {'all':champ, 'myFilter':myFilter,'cartItems':cartItems,}
    return render(request,'design/home.html',context)
# Create your views here.

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order,'cartItems':cartItems}

    return render(request, 'design/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order,'cartItems':cartItems}

    return render(request, 'design/checkout.html', context)

def confirmation(request):
    context = {}
    return render(request, 'design/confirmation.html', context)

def updateItem(request):
    data = json.loads(request.body)
    championId = data['championId']
    action = data['action']

    print('Action:', action)
    print('championId:', championId)



    customer = request.user.customer
    product = Champions.objects.get(id=championId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item was added', safe=False)

def processOrder(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        order.complete=True
        order.save()
    else:
        print("user is not logged in")
    return JsonResponse('ORDER COMPLETE', safe=False)

def addUserInfoForm(request):
    if request.method =='POST':
        post = UserInfo()
        post.uName = request.POST.get('full_name')
        post.uEmail=request.POST.get('email')
        post.uPhone=request.POST.get('phone_number')
        post.uAddress1=request.POST.get('address_line_1')
        post.uAddress2=request.POST.get('address_line_2')
        post.uCity =request.POST.get('city')
        post.uState=request.POST.get('state')
        post.uZip =request.POST.get('postal_code')
        post.uCardType=request.POST.get('card_type')
        post.uNameOnCard=request.POST.get('name_on_card')
        post.uCardNumber=request.POST.get('card_number')
        post.uExpiration_date=request.POST.get('expiration_date')
        post.uCvc_number=request.POST.get('cvc_number')
        post.uDelivery_option=request.POST.get('delivery_option')
        post.save()

    # userinfo = UserInfo(UName = Name,uEmail = Email,uPhone = phone, uAddress1 = Address1, uAddress2 = Address2,
    #     uCity = City, uState= State, uZip = Zip, uCardType = CardType, uNameOnCard = NameOnCard, uCardNumber=CardNumber,
    #     uExpiration_date=Expiration_date,uCvc_number=Cvc_number,uDelivery_option=Delivery_option)
    # userinfo.save()
    return render(request,'design/checkout.html')
