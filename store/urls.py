
from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('product_detail/<int:id>/', views.product_detail, name="product_detail_url"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('bee_store/', views.beeStore, name="bee_store_url"),
	path('bee_queen/', views.queenStore, name="bee_queen_url"),

]