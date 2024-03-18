from django.db.models import Sum
from django.forms import model_to_dict
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import (Vendor, Payment, PaymentCycle, PaymentMethod, PaidOrders)
from .serializers import (VendorSerializer, PaymentSerializer, PaymentCycleSerializer
, CreatePaymentSerializer,
                          PaidOrdersSerializer,
                          PaymentMethodSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from core.models import User
from django.utils.html import format_html
import datetime
import pandas as pd
import pandas_gbq
import numpy as np
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class PaymentMethodAPI(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class PaymentCycleAPI(generics.ListCreateAPIView):
    queryset = PaymentCycle.objects.all()
    serializer_class = PaymentCycleSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class VendorAPI(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class PaymentAPI(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]



class CreatePaymentAPI(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def perform_create(self, serializer):
        vendor_id = serializer.validated_data.get('vendor_id')
        start_date = serializer.validated_data.get('date_from')
        end_date = serializer.validated_data.get('date_to')

        existing_payment = Payment.objects.filter(
            vendor_id=vendor_id,
            date_from=start_date,
            date_to=end_date
        ).first()

        if existing_payment:
            raise ValidationError('A payment with the same vendor, start date, and end date already exists.')

        serializer.save()

class UploadVendorsAsExcel(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            for index, row in df.iterrows():

                account_manager = row['account_manager']
                pay_type = row['pay_type']
                pay_period = row['pay_period']

                #               get account manager id
                account_manager_id = User.objects.get(username=account_manager).id
                pay_type_id = PaymentMethod.objects.get(title=pay_type).id
                pay_period_id = PaymentCycle.objects.get(title=pay_period).id

                if Vendor.objects.filter(vendor_id=row['vendor_id']).exists():
                    continue

                vendors = Vendor.objects.create(
                    vendor_id=row['vendor_id'],
                    name=row['name'],
                    account_manager_id=account_manager_id,
                    pay_period_id=pay_period_id,
                    pay_type_id=pay_type_id,
                    number=row['number'],
                    fully_refunded=False,
                    penalized=False,
                    owner_name=row['owner_name'],
                    owner_phone=row['owner_phone'],
                    created_by=request.user,
                )
                vendors.save()

            return Response({'message': 'File Uploaded Successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorPaymentsSummaryAPI(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        query = f"""
           SELECT * FROM `peak-brook-355811.food_prod_public.vendor_payment` 
           WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
           """
        df = pandas_gbq.read_gbq(query, project_id='peak-brook-355811')

        # Replace NaN (null in DataFrame) with None for direct JSON serialization
        df.replace({np.nan: None}, inplace=True)

        # Calculate the count of orders for each vendor and aggregate order details
        df['order_details'] = df.apply(lambda row: row.to_dict(), axis=1)
        orders_by_vendor = df.groupby('vendor_id')['order_details'].apply(list).reset_index(name='orders')
        order_counts = df.groupby('vendor_id')['order_id'].count().reset_index(name='order_count')

        # Group and sum the `to_be_paid` column by vendor
        grouped_sum = df.groupby('vendor_id', as_index=False)['to_be_paid'].sum()

        # Merge the sum DataFrame with the order counts DataFrame
        grouped_sum = pd.merge(grouped_sum, order_counts, on='vendor_id')

        # Merge with the orders data
        grouped_sum = pd.merge(grouped_sum, orders_by_vendor, on='vendor_id')

        # Fetch additional vendor details from the Django model
        # Fetch additional vendor details from the Django model
        vendors = Vendor.objects.prefetch_related('pay_period', 'pay_type').in_bulk(field_name='id')
        vendor_details = {vendor.vendor_id: {
            'vendor_id': vendor.vendor_id,
            'vendor': vendor.name,
            'number': vendor.number,
            'penalized': vendor.penalized,
            'fully_refunded': vendor.fully_refunded,
            'pay_period': PaymentCycleSerializer(vendor.pay_period).data.get('title', ''),
            'pay_type': PaymentMethodSerializer(vendor.pay_type).data.get('title', ''),
        } for vendor in vendors.values()}



        # Query the payments table for matching records
        paid_vendors = Payment.objects.filter(
            Q(date_from=start_date) & Q(date_to=end_date) & Q(is_paid=True)
        ).values_list('vendor_id', flat=True)

        # Prepare the final results, adding start_date, end_date, order count, orders, and is_paid for each vendor
        final_results = []
        for item in grouped_sum.itertuples(index=False):
            vendor_info = vendor_details.get(str(item.vendor_id), {})
            if item.vendor_id not in paid_vendors:  # Only include vendors that are not in the paid_vendors list
                # Retrieve existing order IDs for this vendor and date range
                existing_orders = Payment.objects.filter(
                    vendor_id=item.vendor_id
                ).values_list('orders', flat=True)
                existing_order_ids = set([order['order_id'] for order_list in existing_orders for order in order_list])


                # Filter new orders to include only those not already in existing_order_ids
                new_orders = [order for order in item.orders if order['order_id'] not in existing_order_ids]


                result_item = {
                    **item._asdict(),
                    **vendor_info,
                    'start_date': start_date,
                    'end_date': end_date,
                    'is_paid': False,
                    'orders': new_orders,  # Updated orders list
                }
                final_results.append(result_item)

        return Response(final_results)