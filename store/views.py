from datetime import datetime
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.http import JsonResponse
from .models import *
from .utils import cartData, guestOrder
import json


class Store(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        context['products'] = Product.objects.all()
        return context

    template_name = 'store/store.html'


class Cart(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['items'] = data['items']
        context['order'] = data['order']
        context['cartItems'] = data['cartItems']
        context['shipping'] = False
        return context

    template_name = 'store/cart.html'


class Checkout(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['items'] = data['items']
        context['order'] = data['order']
        context['cartItems'] = data['cartItems']
        context['shipping'] = False
        return context

    template_name = 'store/checkout.html'


class updateItem(UpdateView):
    def form_valid(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        print('action: ', action)
        print('poductId: ', productId)

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)


class processOrder(View):
    def post(self, request):
        transaction_id = datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
        return JsonResponse('Payment complete!', safe=False)
