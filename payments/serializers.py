from rest_framework import serializers

from .models import Gateway, Payment


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('title', 'avatar')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'user',
            'package',
            'gateway', 
            'price', 
            'status', 
            'token', 
            'device_uuid', 
            'phone_number', 
            'consumed_code'
        )