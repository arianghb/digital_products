from django.urls import path

from .views import GatewayView, PaymentView

urlpatterns = [
    path('gateways/', GatewayView.as_view(), name='gatway-view'),
    path('payment/', PaymentView.as_view(), name='payment-view'),
]