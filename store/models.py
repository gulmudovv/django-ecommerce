from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	title = models.CharField(max_length=200, null=True)
	
	def __str__(self):
		return self.title

   
  # Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)


	def __str__(self):
		return self.name



class Product(models.Model):
	category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=200, null=True)
	price = models.FloatField()
	description = models.TextField()
	digital = models.BooleanField(default=False, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)
	massa = models.CharField(max_length=20, null=True)

	def __str__(self):
		return self.title

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''

		return url
	



class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_orderd = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)
	
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		
		
		for i in orderitems:
			if i.product.digital == False:
				shipping = True 
		return shipping
	


	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	

	def __str__(self):
		return str(self.id)




class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	

class ShippingAdress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	city = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=500, null=True)
	subway = models.CharField(max_length=200, null=True)
	phonenumber = models.CharField(max_length=200, null=True)	
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.address
   