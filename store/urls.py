from django.urls import path

from store.views import Store, Cart, Checkout, updateItem, processOrder

urlpatterns = [
    path('', Store.as_view(), name='store'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('update_item/', updateItem.as_view(), name='update_item'),
    path('process_order/', processOrder.as_view(), name='process_order'),
]
