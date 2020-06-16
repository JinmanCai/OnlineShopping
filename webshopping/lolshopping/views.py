from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from .filters import ChampionsFilter





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
