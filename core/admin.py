from django.contrib import admin
from .models import Item, Order, OrderItem, BillingAddress

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Item, ItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'ordered_date', 'is_ordered']
admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)
admin.site.register(BillingAddress)