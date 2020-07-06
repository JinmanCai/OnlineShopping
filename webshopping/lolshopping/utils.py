import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('cart:',cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']


    for i in cart:
        cartItems += cart[i]["quantity"]

        champ = Champions.objects.get(id = i)
        total = (champ.price * cart[i]["quantity"])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]["quantity"]

        item = {
            'product':{
                'id': champ.id,
                'name': champ.name,
                'role': champ.role,
                'price': champ.price,
                'imageURL': champ.imageURL,
                },
            'quantity':cart[i]["quantity"],
            'get_total':total
        }
        items.append(item)
    return {'cartItems':cartItems, 'order':order, 'items': items}
