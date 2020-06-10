from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem
from django.conf import settings
from django.contrib.sessions.models import Session 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import BillingAddressForm
from.models import BillingAddress
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, View

class ProductView(ListView):
    model = Item
    template_name = 'products.html'
    context_object_name = 'items'

class ProductDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'
    context_object_name = 'item'

class OrderSummary(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(owner=self.request.user, is_ordered=False)
            order_list = order.items.all()
            context = {'order':order, "order_list":order_list}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You did not have any item in your cart.')
            return redirect('/')
        

class BillingAddress(View):
    def get(self, request, *args, **kwargs):
        form = BillingAddressForm()
        context = {'form':form}
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(owner=request.user, is_ordered=False)
        except ObjectDoesNotExist:
            messages.warning(request, 'You did not have an active order')
            return redirect('core:order_summary')
        form = BillingAddressForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            billing_address = form.save(commit=False)
            billing_address.owner = request.user
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            messages.success(request, 'Address received')
            return redirect('core:payment')
        messages.warning(request, 'The form is invalid!')
        return redirect('core:billing_address')

        
class PaymentView(View):
    def get(self, request, *args, **kwargs):
        host = request.get_host()
        form = PayPalPaymentsForm()
        context = {"form":form}
        return render(request, 'payment.html', context) 

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, owner=request.user, is_ordered=False)
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,        
            'amount': order.get_total()
        }

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created  = OrderItem.objects.get_or_create(item=item, owner=request.user, is_ordered=False)
    order_qs = Order.objects.filter(owner=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, 'Your order item has been updated.')
            return redirect('core:order_summary')
        else:
            order.items.add(order_item)
            messages.info(request, 'Your order has been updated created successfully proceed to checkout.')
            return redirect('core:order_summary')

    else:
        order = Order.objects.create(owner=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.success(request, 'Your order has been received proceed to checkout.')
        return redirect('core:order_summary')
     
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(owner=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            order_item = OrderItem.objects.get(item=item, owner=request.user, is_ordered=False)
            order.items.remove(order_item)
            messages.success(request, 'This item was removed from your cart.')
            return redirect('core:order_summary')
        else:
            messages.info(request, 'This item was not in your cart.')
            return redirect('core:order_summary')
    else:
        messages.info(request, 'You did not have an active order')
        return redirect('core:order_summary')

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(owner=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            order_item = OrderItem.objects.get(item=item, owner=request.user, is_ordered=False)
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.success(request, 'This item quantity was updated.')
            return redirect('core:order_summary')
        else:
            messages.info(request, 'This item was not in your cart.')
            return redirect('core:order_summary')
    else:
        messages.info(request, 'You did not have an active order')
        return redirect('core:order_summary')