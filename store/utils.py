import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart= {}

    print(cart)
    items = []
    order = {'get_cart_total':0,'get_total':0}
    cart_total = order['get_cart_total']

    try:
        for i in cart:
            cart_total += cart[i]["quantity"]
            product = Product.objects.get(id = i)

            total = (product.price * cart[i]["quantity"])
            order['get_total'] +=  total
            order['get_cart_total'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

    except:
        pass
    return{'cart_items':items, 'order':order, 'cart_total':cart_total}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        order_items = order.orderitem_set.all()

        cart_total = order.get_cart_total
    else:
        cookieData = cookieCart(request)
        order_items = cookieData['cart_items']
        order = cookieData['order']
        cart_total = cookieData['cart_total']
        
    return{'cart_items':order_items, 'order':order, 'cart_total':cart_total}

def getOrder (request,data):
    name = data["user_data"]["user_name"]
    email = data["user_data"]["user_email"]

    cookieData = cookieCart(request)
    items = cookieData["cart_items"]

    customer,created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer,complete = False)
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order
        )
    return customer , order 