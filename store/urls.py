from django.urls import path

from store.views import Store, Cart, Checkout, updateItem, processOrder, ProductPage, Register

urlpatterns = [
    path('', Store.as_view(), name='store'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
	path('register/', Register.as_view(), name='register'),
    path('update_item/', updateItem.as_view(), name='update_item'),
    path('process_order/', processOrder.as_view(), name='process_order'),
    path('product-<int:pk>/', ProductPage.as_view(), name='product_page'),
]
