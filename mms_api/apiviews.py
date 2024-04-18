from rest_framework import generics, status
from django.template.loader import render_to_string
from rest_framework.views import APIView

from .models import (Vendor, Payment, PaymentCycle,
                     PaymentMethod, PaidOrders,
                     VendorUpdates, VendorIDName,
                     VendorDetails)
from .serializers import (VendorSerializer, PaymentSerializer,
                          PaymentCycleSerializer,
                          CreatePaymentSerializer,
                          VendorIDNameSerializer,
                          PaidOrdersSerializer,
                          PaymentMethodSerializer,
                          VendorIDNameSerializer,
                          VendorDetailsUpdateSerializer,
                          GetVendorUpdatesSerializer,
                          CreateVendorUpdateSerializer,
                          VendorIDNameSerializer,
                          VendorDetailsSerializer, UnmatchedVendorCountSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from core.models import User
import pandas as pd
import pandas_gbq
import numpy as np
from django.db.models import Count, Q, OuterRef, Exists
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.mail import send_mail


# get vendors count that does not have details
class UnmatchedVendorsAPIView(APIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        # Create a subquery for VendorDetails that refer to VendorIDName
        vendor_details_subquery = VendorDetails.objects.filter(vendor_id=OuterRef('pk'))
        # Get all VendorIDName that do not have a corresponding VendorDetails
        return VendorIDName.objects.annotate(
            is_matched=Exists(vendor_details_subquery)
        ).filter(is_matched=False)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Use the get_queryset method
        # Serialize the data
        serializer = VendorIDNameSerializer(queryset, many=True)
        return Response(serializer.data)


class MatchedVendorsAPIView(APIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        # Create a subquery for VendorDetails that refer to VendorIDName
        vendor_details_subquery = VendorDetails.objects.filter(vendor_id=OuterRef('pk'))
        # Get all VendorIDName that do not have a corresponding VendorDetails
        return VendorIDName.objects.annotate(
            is_matched=Exists(vendor_details_subquery)
        ).filter(is_matched=True)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Use the get_queryset method
        # Serialize the data
        serializer = VendorIDNameSerializer(queryset, many=True)
        return Response(serializer.data)


# get all vendors with its details
class VendorDetailsAPI(generics.ListCreateAPIView):
    queryset = VendorDetails.objects.all().order_by('-vendor_id')
    serializer_class = VendorDetailsSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class GetVendorUpdatesAPI(generics.ListCreateAPIView):
    queryset = VendorUpdates.objects.all().order_by('-created_at')
    serializer_class = GetVendorUpdatesSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.order_by('created_at')  # Order by vendor_id


class GetSingleVendorUpdatesAPI(generics.ListCreateAPIView):
    serializer_class = GetVendorUpdatesSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        vendor_id = self.kwargs.get('pk')
        queryset = VendorUpdates.objects.filter(
            vendor_id=vendor_id).order_by('-created_at')
        return queryset


class CreateVendorUpdateAPI(generics.ListCreateAPIView):
    queryset = VendorUpdates.objects.all()
    serializer_class = CreateVendorUpdateSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    paginator = PageNumberPagination()
    paginator.page_size = None

    def perform_create(self, serializer):
        # Save the new object
        instance = serializer.save()

        # Convert serializer data to DataFrame
        df = pd.DataFrame([serializer.data])

        table_data = {
            "Field": [
                'Payment Cycle',
                'Payment Method',
                'Number',
                'Receiver Name',
                'Account Manager',
                'Fully Refended',
                'Penalized',
                'Commission After Discount',
                'Emails',
            ],
            'Old Value': [
                df.loc[0, 'old_payment_cycle'],
                df.loc[0, 'old_payment_method'],
                df.loc[0, 'old_number'],
                df.loc[0, 'old_receiver_name'],
                df.loc[0, 'old_account_manager'],
                df.loc[0, 'old_fully_refended'],
                df.loc[0, 'old_penalized'],
                df.loc[0, 'old_commission_after_discount'],
                df.loc[0, 'old_emails'],
            ],
            "New Value": [
                df.loc[0, 'new_payment_cycle'],
                df.loc[0, 'new_payment_method'],
                df.loc[0, 'new_number'],
                df.loc[0, 'new_receiver_name'],
                df.loc[0, 'new_account_manager'],
                df.loc[0, 'new_fully_refended'],
                df.loc[0, 'new_panelized'],
                df.loc[0, 'new_commission_after_discount'],
                df.loc[0, 'new_emails'],
            ],
        }

        # Convert table_data to DataFrame
        df_table = pd.DataFrame(table_data)

        # Convert DataFrame to HTML table
        df_html = df_table.to_html(index=False, escape=False)

        vendor_name = df.loc[0, 'vendor_name']
        # vendor_id = df.loc[0, 'vendor_id']
        created_by_id = df.loc[0, 'created_by']
        created_by_username = User.objects.get(id=created_by_id).username
        subject_title = f"New Update On {vendor_name} Created By {created_by_username}"

        # Construct email subject
        subject = subject_title

        # Render email message template with HTML table
        message = render_to_string('email_template.html', {'df_html': df_html})

        # Send email
        recipient_list = ['zakarya.bilal@baly.iq',
                          'omar.mahir@baly.iq'
                          ]
        send_mail(
            subject,
            message,
            'food-bi@baly.iq',
            recipient_list,
            html_message=message,  # Set html_message parameter to include HTML content
            fail_silently=False,
        )


class VendorIdNameAPI(generics.ListCreateAPIView):
    queryset = VendorIDName.objects.all()
    serializer_class = VendorIDNameSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    paginator = PageNumberPagination()
    paginator.page_size = None


class VendorByIdAPI(generics.ListCreateAPIView):
    serializer_class = VendorDetailsSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        # Assuming you're passing vendor_id as a URL parameter
        vendor_id = self.kwargs.get('pk')
        queryset = VendorDetails.objects.filter(vendor_id=vendor_id)
        return queryset


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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('vendor_id')  # Order by vendor_id


class UpdateVendorAPI(generics.RetrieveUpdateAPIView):
    lookup_field = 'vendor_id'
    queryset = VendorDetails.objects.all()
    serializer_class = VendorDetailsUpdateSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class PaymentAPI(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')


class CreatePaymentAPI(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            created_payments = []
            for item in request.data:
                serializer = self.get_serializer(data=item)
                serializer.is_valid(raise_exception=True)

                try:
                    self.perform_create(serializer)

                    created_payments.append(serializer.data)
                except ValidationError as e:
                    # If a ValidationError occurs, log the error and continue with the next item
                    # print(f"Error creating payment: {e}")
                    continue
            return Response(created_payments, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        vendor_id = serializer.validated_data.get('vendor_id')
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')

        existing_payment = Payment.objects.filter(
            vendor_id=vendor_id,
            start_date=start_date,
            end_date=end_date
        ).first()

        if existing_payment:
            return
            # raise ValidationError('A payment with the same vendor, start date, and end date already exists.')

        serializer.save()


class UploadVendorsAsExcel(generics.ListCreateAPIView):
    queryset = VendorDetails.objects.all()
    serializer_class = VendorDetailsSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            for index, row in df.iterrows():

                vendor_instance = VendorIDName.objects.get(id=row['vendor_id'])
                pay_type_id = PaymentMethod.objects.get(title=row['pay_type'].strip()).id
                pay_period_id = PaymentCycle.objects.get(title=row['pay_period'].strip()).id

                if VendorDetails.objects.filter(vendor_id=row['vendor_id']).exists():
                    continue

                vendors = VendorDetails.objects.create(
                    vendor_id=vendor_instance,
                    account_manager_id=row['account_manager'],
                    pay_period_id=pay_period_id,
                    pay_type_id=pay_type_id,
                    number=row['number'],
                    fully_refunded=row['fully_refunded'],
                    commission_after_discount=row['commission_after_discount'],
                    penalized=False,
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
           SELECT order_id, order_date,vendor, vendor_id,subtotal,to_be_paid FROM 
           `peak-brook-355811.food_prod_public.vendor_payment`
           WHERE order_date BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59'
           """
        df = pandas_gbq.read_gbq(query, project_id='peak-brook-355811')

        # Replace NaN (null in DataFrame) with None for direct JSON serialization
        df.replace({np.nan: None}, inplace=True)

        # Calculate the count of orders for each vendor and aggregate order details
        df['order_details'] = df.apply(lambda row: row.to_dict(), axis=1)
        orders_by_vendor = df.groupby('vendor_id')['order_details'].apply(
            list).reset_index(name='orders')
        order_counts = df.groupby('vendor_id')[
            'order_id'].count().reset_index(name='order_count')

        # Group and sum the `to_be_paid` column by vendor
        grouped_sum = df.groupby('vendor_id', as_index=False)[
            'to_be_paid'].sum()

        # Merge the sum DataFrame with the order counts DataFrame
        grouped_sum = pd.merge(grouped_sum, order_counts, on='vendor_id')

        # Merge with the orders data
        grouped_sum = pd.merge(grouped_sum, orders_by_vendor, on='vendor_id')

        # Fetch additional vendor details from the Django model
        vendors = Vendor.objects.prefetch_related(
            'pay_period', 'pay_type').in_bulk(field_name='id')
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
            Q(start_date=start_date) & Q(end_date=end_date)
        ).values_list('vendor_id', flat=True)

        # Prepare the final results, adding start_date, end_date, order count, orders, and is_paid for each vendor
        final_results = []
        for item in grouped_sum.itertuples(index=False):

            vendor_info = vendor_details.get(str(item.vendor_id), {})
            # Retrieve existing order IDs for this vendor and date range
            # existing_orders = Payment.objects.filter(
            #     vendor_id=item.vendor_id,
            # ).values_list('orders', flat=True)
            #
            # new_orders = [
            #     order for order in item.orders if order['order_id'] not in existing_orders]

            existing_vendor_orders = Payment.objects.filter(
                vendor_id=item.vendor_id,
            ).values_list('orders', flat=True)

            new_orders = []
            for order in item.orders:
                for ex_order in existing_vendor_orders:
                    if order['order_id'] not in ex_order:
                        new_orders.append(order)

            new_orders_list = [
                {
                    'order_id': order['order_id'],
                    'order_date': order['order_date'],
                    'subtotal': order['subtotal']
                }
                for order in new_orders
            ]

            result_item = {
                **item._asdict(),
                **vendor_info,
                'start_date': start_date,
                'end_date': end_date,
                'is_paid': False,
                'orders': new_orders_list,
            }
            final_results.append(result_item)

        return Response(final_results)


class UpdateVendorTableFromBigQueryAPI(generics.ListCreateAPIView):
    queryset = VendorIDName.objects.all()
    serializer_class = VendorIDNameSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    paginator = PageNumberPagination()
    paginator.page_size = None

    def list(self, request, *args, **kwargs):

        query = f""" SELECT id,enName,arName  from `food_prod_public.vendors` """
        df = pandas_gbq.read_gbq(query, project_id='peak-brook-355811')

        # Replace NaN with None for database insertion compatibility
        df = df.where(pd.notnull(df), None)

        # Insert new data into OnlyVendor model
        new_records = 0
        for _, row in df.iterrows():
            # Check if the vendor already exists
            if not VendorIDName.objects.filter(id=row['id']).exists():
                VendorIDName.objects.create(
                    id=row['id'],
                    enName=row['enName'],
                    arName=row['arName']
                )
                new_records += 1

        # Response message
        response_msg = f"Inserted {new_records} new vendor(s)."
        return Response({'message': response_msg, 'new_records': new_records})
