from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, cookieCart, guestOrder
from  .models import *
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail



def store(request):
	data = cartData(request)
	cartItems = data['cartItems']	
	
	products = Product.objects.filter(category_id=1)	
		
	context = {'products': products,"cartItems": cartItems }
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']		
	context = {'cartItems':cartItems,'order': order,'items': items}
	return render(request, 'store/cart.html', context)


def checkout(request):	
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']		
	context = {'cartItems':cartItems, 'order': order, 'items': items}
	return render(request, 'store/checkout.html', context)




def product_detail(request, id):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	product = Product.objects.get(id__iexact=id)	
	context = {'product': product, "order": order,"cartItems": cartItems}
	return render(request, 'store/product_detail.html', context)

def beeStore(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	beepocket = Product.objects.get(category_id=2)
		
	context = {'beepocket': beepocket, "order": order,"cartItems": cartItems}	
	return render(request, 'store/bee_store.html', context)

def queenStore(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	beequeen = Product.objects.get(category_id=3)
		
	context = {'beequeen': beequeen, "order": order,"cartItems": cartItems}	
	return render(request, 'store/bee_queen.html', context)




def updateItem(request):
	
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']	

	customer =request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	if action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	
	return JsonResponse("Items was added", safe=False)

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created  = Order.objects.get_or_create(customer=customer, complete=False)		
	

	else:
		customer, order, sendOrder = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id 

	if total == float(order.get_cart_total):			
		order.complete = True		
	order.save()

	if order.shipping == True:
		ShippingAdress.objects.create(
			customer = customer,
			order = order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			subway=data['shipping']['subway'],
			phonenumber=data['shipping']['phonenumber'],
			zipcode=data['shipping']['zipcode'],)
	
	# Данные для отправки информации о заказе на почтовый ящик
	msg = render_to_string('store/send_order.html', {'name': customer, 
			'email': customer.email,
			'order':order,
			'address':data['shipping']['address'],
			'city':data['shipping']['city'],
			'subway':data['shipping']['subway'],
			'phonenumber' :data['shipping']['phonenumber'],
			'zipcode': data['shipping']['zipcode'],
			'sendOrder': sendOrder,
			'total': int(total),
			'dateOrder': datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S"),
			})
	# Функция для отправки информации о заказе на почтовый ящик	
	send_mail('Интернет Магазин Мёда', msg, settings.EMAIL_HOST_USER, ['khavabee@yandex.ru'])

	return JsonResponse("Payment complete", safe=False)



