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

    champ = myFilter.qs

    context = {'all':champ, 'myFilter':myFilter,'cartItems':cartItems}
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
