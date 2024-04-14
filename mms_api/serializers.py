from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import (Vendor, Payment,
                     PaymentMethod, PaymentCycle,
                     PaidOrders, VendorUpdates)

from core.serializers import CustomUserSerializer


class VendorCustomSerializer(serializers.ModelSerializer):
    total_to_be_paid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
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


class GetVendorUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorUpdates
        fields = '__all__'


class CreateVendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorUpdates
        fields = ['vendor_id', 'old_payment_method', 'new_payment_method', 'old_payment_cycle', 'new_payment_cycle', 'old_number', 'new_number',
                  'old_receiver_name', 'new_receiver_name',
                  'old_owner_phone', 'new_owner_phone', 'old_account_manager', 'new_account_manager',
                  'old_fully_refended', 'new_fully_refended',
                  'old_penalized', 'new_panelized', 'old_emails', 'new_emails', 'created_by'
                  ]


class VendorSerializer(serializers.ModelSerializer):
    # Assuming this is your payment_cycle serializer
    pay_period = PaymentCycleSerializer(read_only=True)
    # Assuming this is your payment_method serializer
    pay_type = PaymentMethodSerializer(read_only=True)
    # Use SerializerMethodField
    account_manager_name = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'pay_period', 'pay_type', 'number',
                  'owner_name', 'owner_phone', 'owner_email_json', 'fully_refunded', 'penalized',
                  'account_manager_name', 'created_at',
                  ]

    def get_account_manager_name(self, obj):
        # Check if account_manager is set, handle potential None values
        if obj.account_manager:
            return obj.account_manager.username  # Access the username attribute
        else:
            return None  # Return None or a default value if account_manager is missing


class VendorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'pay_period', 'pay_type', 'number',
                  'owner_name', 'owner_phone', 'owner_email_json', 'fully_refunded', 'penalized',
                  'account_manager', 'created_at',
                  ]


class VendorIDNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'vendor_id', 'vendor', 'start_date', 'end_date', 'pay_period', 'pay_type', 'number', 'to_be_paid', 'is_paid', 'order_count', 'created_at', 'created_by', 'orders'
                  ]


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaidOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidOrders
        fields = '__all__'
