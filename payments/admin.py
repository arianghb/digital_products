from django.contrib import admin

from .models import Gateway, Payment


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass