from django.contrib import admin
from .models import (Vendor, Payment,
                     PaymentCycle, PaidOrders,
                     PaymentMethod, VendorUpdates,
                     VendorIDName, VendorDetails)
from django.utils.html import format_html

import datetime
import pandas as pd
import pandas_gbq


@admin.register(VendorUpdates)
class VendorUpdatesAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    ordering = ('-created_at',)  # Default ordering
    search_fields = ['vendor_id']  # Fields to search by
    list_display = ['vendor_id']


@admin.register(VendorIDName)
class VendorIDNameAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    ordering = ('id',)  # Default ordering
    search_fields = ['id']  # Fields to search by
    list_display = ['id', 'arName', 'enName']


@admin.register(VendorDetails)
class VendorDetailsAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    ordering = ('vendor_id',)  # Default ordering
    search_fields = ['vendor_id']  # Fields to search by
    list_display = [field.name for field in VendorDetails._meta.get_fields(
    ) if field.name != 'id'
                    ]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    ordering = ('-created_at',)  # Default ordering
    search_fields = ['vendor_id']  # Fields to search by
    list_display = ['vendor_id', 'name', 'number']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    ordering = ('-created_at',)  # Default ordering
    search_fields = ['vendor_id']  # Fields to search by
    list_display = [field.name for field in Payment._meta.get_fields(
    ) if field.name != 'id' and field.name != 'orders']

    # def save_model(self, request, obj, form, change):
    #     # Execute SQL query and load data into DataFrame
    #     df = pandas_gbq.read_gbq("""
    #       SELECT o.id, v.id AS vendor_id, v.arName AS vendor_name, o.created_at, o.totalValue
    #       FROM `peak-brook-355811.food_prod_public.orders` o
    #       INNER JOIN `peak-brook-355811.food_prod_public.vendors` v
    #       ON o.vendorID = v.id
    #       WHERE o.created_at BETWEEN '2024-01-01' AND '2024-01-15'
    #       LIMIT 10000
    #       """,
    #       project_id='peak-brook-355811')
    #
    #     # Iterate over the DataFrame rows and create Payment instances
    #     for _, row in df.iterrows():
    #         Payment.objects.create(
    #             vendor_id=row['vendor_id'],
    #             vendor_name=row['vendor_name'],
    #             date_from=row['created_at'],  # Assuming date_from is the order's created_at
    #             date_to=row['created_at'],  # Assuming date_to is the same as date_from
    #             payment_cycle=PaymentCycle.objects.first(),  # Use the first PaymentCycle as an example
    #             payment_method=PaymentMethod.objects.first(),  # Use the first PaymentMethod as an example
    #             number=0,  # Assuming a default value for number
    #             amount=row['totalValue'],
    #             created_by=request.user
    #         )
    #
    #     super().save_model(request, obj, form, change)


@admin.register(PaymentCycle)
class PaymentCycleAdmin(admin.ModelAdmin):
    # list_per_page = 5  # Items per page
    # search_fields = ['title']  # Fields to search by
    list_display = ['title']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_per_page = 5  # Items per page
    search_fields = ['title']  # Fields to search by
    list_display = ['title']


@admin.register(PaidOrders)
class PaidOrdersAdmin(admin.ModelAdmin):
    list_per_page = 25  # Items per page
    ordering = ('-created_at',)  # Default ordering
    search_fields = ['payment_id']  # Fields to search by
    list_display = [
        field.name for field in PaidOrders._meta.get_fields() if field.name != 'id']

    def formatted_price_dinar(self, obj):
        return format_html(f"IQD {obj.amount:,.0f}")

    formatted_price_dinar.short_description = 'Amount'  # Sets the column header
