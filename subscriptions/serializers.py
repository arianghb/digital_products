from rest_framework import serializers

from .models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('sku', 'title', 'description', 'avatar', 'duration')


class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer()

    class Meta:
        model = Subscription
        fields = ('user', 'package')
