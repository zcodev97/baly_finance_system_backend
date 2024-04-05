from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import (Vendor, Payment, PaymentMethod, PaymentCycle, PaidOrders)

from core.serializers import CustomUserSerializer


class VendorCustomSerializer(serializers.ModelSerializer):
    total_to_be_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    orders = serializers.JSONField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['name', 'total_to_be_paid', 'orders']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCycle
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    pay_period = PaymentCycleSerializer(read_only=True)  # Assuming this is your payment_cycle serializer
    pay_type = PaymentMethodSerializer(read_only=True)  # Assuming this is your payment_method serializer
    account_manager_name = serializers.SerializerMethodField()  # Use SerializerMethodField

    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'pay_period', 'pay_type', 'number',
                  'owner_name', 'owner_phone', 'fully_refunded', 'penalized',
                  'account_manager_name', 'created_at','owner_email','log'
                  ]

    def get_account_manager_name(self, obj):
        # Check if account_manager is set, handle potential None values
        if obj.account_manager:
            return obj.account_manager.username  # Access the username attribute
        else:
            return None  # Return None or a default value if account_manager is missing


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'vendor_id', 'vendor', 'start_date', 'end_date'
            , 'pay_period', 'pay_type', 'number', 'to_be_paid', 'is_paid', 'order_count'
            , 'created_at', 'created_by', 'orders'
                  ]


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaidOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidOrders
        fields = '__all__'
