from django.urls import path
from . views import ProductView, ProductDetailView, OrderSummary, BillingAddress, add_to_cart, remove_from_cart, remove_single_item_from_cart

app_name = 'core'

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('order-summary/', OrderSummary.as_view(), name='order_summary'),
    path('billing-address/', BillingAddress.as_view(), name='billing_address'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug:slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
]
