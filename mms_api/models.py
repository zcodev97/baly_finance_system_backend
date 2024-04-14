import uuid
from django.db.models import Sum
from django.conf import settings
from django.db import models, transaction
from django.db import models
from django.contrib.auth.models import User


class PaymentCycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pay_period = models.ForeignKey(PaymentCycle, on_delete=models.CASCADE)
    pay_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255)
    owner_phone = models.CharField(max_length=255)
    # owner_email = models.CharField(max_length=255)
    owner_email_json = models.JSONField(default=list)
    fully_refunded = models.BooleanField()
    penalized = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    # log = models.JSONField()
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_manager')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VendorUpdates(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_id = models.CharField(max_length=255)
    old_payment_method = models.CharField(max_length=255)
    new_payment_method = models.CharField(max_length=255)
    old_payment_cycle = models.CharField(max_length=255)
    new_payment_cycle = models.CharField(max_length=255)
    old_number = models.CharField(max_length=255)
    new_number = models.CharField(max_length=255)
    old_receiver_name = models.CharField(max_length=255)
    new_receiver_name = models.CharField(max_length=255)
    old_owner_phone = models.CharField(max_length=255)
    new_owner_phone = models.CharField(max_length=255)
    old_account_manager = models.CharField(max_length=255)
    new_account_manager = models.CharField(max_length=255)
    old_fully_refended = models.CharField(max_length=255)
    new_fully_refended = models.CharField(max_length=255)
    old_penalized = models.CharField(max_length=255)
    new_panelized = models.CharField(max_length=255)
    old_emails = models.CharField(max_length=255)
    new_emails = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name_plural = 'Vendor Updates'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_id = models.IntegerField()
    vendor = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pay_period = models.CharField(max_length=255)
    pay_type = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True)
    to_be_paid = models.CharField(max_length=255)
    is_paid = models.BooleanField()
    order_count = models.JSONField()
    orders = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.vendor


class PaidOrders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_id = models.CharField(max_length=10, unique=True, editable=False)
    order_id = models.CharField(max_length=255, unique=True)
    order_date = models.DateTimeField()
    vendor = models.CharField(max_length=255)
    vendor_id = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vendor_db_id")
    sub_total = models.FloatField()
    vendor_discount_cap = models.FloatField()
    vendor_discount = models.FloatField()
    total_discount = models.FloatField()
    commission_percentage = models.FloatField()
    commission_value = models.FloatField()
    refund = models.FloatField()
    hybrid_payment = models.FloatField()
    to_be_paid = models.FloatField()
    cancellation_type = models.CharField(max_length=255)
    cancellation_reason = models.CharField(max_length=255)
    lastStatus = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def generate_payment_id(self):
        # Customize the prefix or length as needed
        prefix = "INV"
        # Extract 6 characters from the UUID
        unique_id = str(uuid.uuid4().int)[:8]
        return f"{prefix}-{unique_id}"

    def __str__(self):
        return self.payment_id

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.payment_id:
                # Generate a short and secure invoice ID
                self.payment_id = self.generate_payment_id()
            super().save(*args, **kwargs)
