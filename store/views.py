from django.shortcuts import render 
from django.views import View
from django.http import JsonResponse
import datetime
from .models import *
import json
from .utils import  cartData,cookieCart,getOrder

class StoreView(View):
	template_name = 'store/store.html'
	queryset = Product.objects.all()
	def get(self,request):
		data = cartData(request)
		cart_total = data['cart_total']

		context = {
			"products":self.queryset ,
			"cart_total":cart_total
		}
		return render(request,self.template_name,context)

class CheckoutView(View):
	template_name = 'store/checkout.html'
	def get(self,request):
		data = cartData(request)
		order_items = data['cart_items']
		order = data['order']
		cart_total = data['cart_total']
			
		context = {'items':order_items,'order':order,'cart_total':cart_total}

		return render(request,self.template_name,context)
		

class CartView(View):
	template_name = 'store/cart.html'
	def get(self,request):
		data = cartData(request)
		order_items = data['cart_items']
		order = data['order']
		cart_total = data['cart_total']
			
		context = {'items':order_items,'order':order,'cart_total':cart_total}

		return render(request,self.template_name,context)

class UpdateView(View):
	def post(self,request):
		data = json.loads(request.body)
		product_id = data['product_id']
		action = data['action']

		customer = request.user.customer
		product = Product.objects.get(id = product_id)
		order, created = Order.objects.get_or_create(customer = customer,complete = False)
		# include created when dealing with orders and orderitems incese there exists any.
		order_item ,created = OrderItem.objects.get_or_create(order = order,product = product)

		if action == 'add':
			order_item.quantity = (order_item.quantity + 1)
		elif action == 'remove':
			order_item.quantity = (order_item.quantity - 1)

		order_item.save()

		if order_item.quantity <=0:
			order_item.delete()

		print(action)
		print(product_id)

		return JsonResponse('Item was added', safe = False)

class ProcessOrder(View):
	def post(self,request):
		data = json.loads(request.body)
		transaction_id =datetime.datetime.now().timestamp()

		if request.user.is_authenticated:
			customer = request.user.customer
			order ,created  = Order.objects.get_or_create(customer = customer,complete = False)
			order.transaction_id = transaction_id

		else:
			 customer,order = getOrder(request,data)

		total = float(data['user_data']['total'])
		order.transaction_id = transaction_id
		
		if order.get_total == total:
			order.complete = True
		order.save()
		
		
		ShippingAdress.objects.create(
				customer = customer,
				order = order,
				adress = data['shipping_info']['address'],
				city = data['shipping_info']['city'],
				state = data['shipping_info']['state'],
				zipcode = data['shipping_info']['zip_code']
				)

		return JsonResponse('order was processed',safe = False)
