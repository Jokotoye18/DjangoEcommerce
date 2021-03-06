from django import template
from core.models import Order
from django.contrib.sessions.models import Session 


register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(owner=user, is_ordered=False)
        if order_qs.exists():
            return order_qs[0].items.count()
    return 0