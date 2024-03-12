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
    payment_cycle = models.ForeignKey(PaymentCycle,on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    number = models.IntegerField(max_length=255,blank=True)
    fully_refunded = models.BooleanField()
    penalized = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='account_manager')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_id = models.IntegerField()
    vendor_name = models.CharField(max_length=255)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    payment_cycle = models.ForeignKey(PaymentCycle,on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    number = models.IntegerField(blank=True)
    amount = models.FloatField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor_name


class PaidOrders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_id = models.CharField(max_length=255, unique=True)
    order_id = models.CharField(max_length=255, unique=True)
    amount = models.FloatField(max_length=255)
    paid = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.payment_id


# class CompanyType(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'انواع المشاريع'
#
# #
# class Personal(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, unique=True)
#     container = models.ForeignKey(Container, on_delete=models.CASCADE)
#     total_dinar = models.FloatField()
#     total_dollar = models.FloatField()
#     created_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'خاص'
#
#
# class Company(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, unique=True)
#     container = models.ForeignKey(Container, on_delete=models.CASCADE)
#     total_dinar = models.FloatField()
#     total_dollar = models.FloatField()
#     company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     supervisor = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supervisor')
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'المشاريع'
#
#
# class WithdrawType(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'القيود'
#
#
# class Deposit(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice_id = models.CharField(max_length=10, unique=True, editable=False)
#     container = models.ForeignKey(Container, on_delete=models.CASCADE)
#     company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
#     price_in_dinar = models.FloatField()
#     price_in_dollar = models.FloatField()
#     description = models.TextField(max_length=2000)
#     received_from = models.CharField(max_length=255)
#     created_at = models.DateTimeField()
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_user')
#     record_created_at = models.DateTimeField(auto_now=True)
#     deposit_number = models.PositiveIntegerField(
#         blank=True, unique=True)  # New field
#     document = models.FileField(
#         upload_to='withdraw_documents/', blank=True, null=True)
#
#     # @classmethod
#     # def total_price_in_dinar(cls):
#     #     total_price = cls.objects.aggregate(total_price=Sum('price_in_dinar'))['total_price']
#     #     return total_price or 0
#     def __str__(self):
#         return self.invoice_id
#
#     class Meta:
#         verbose_name_plural = 'الايداعات'
#
#     def generate_invoice_id(self):
#         # Customize the prefix or length as needed
#         prefix = "INV"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:6]
#         return f"{prefix}-{unique_id}"
#
#     def save(self, *args, **kwargs):
#
#         old_price_in_dinar = 0
#         old_price_in_dollar = 0
#         # Retrieve the existing data before update
#         try:
#             old_instance = Deposit.objects.get(pk=self.pk)
#             old_price_in_dinar = old_instance.price_in_dinar
#             old_price_in_dollar = old_instance.price_in_dollar
#         except Deposit.DoesNotExist:
#             # If the instance does not exist yet, set old_instance to None
#             old_instance = None
#
#         if not self.deposit_number:  # Only generate deposit_number if not set
#             last_deposit = Deposit.objects.order_by('-deposit_number').first()
#             if last_deposit:
#                 self.deposit_number = last_deposit.deposit_number + 1
#             else:
#                 self.deposit_number = 1
#
#         with transaction.atomic():
#
#             if not self.invoice_id:
#                 # Generate a short and secure invoice ID
#                 self.invoice_id = self.generate_invoice_id()
#
#                 self.container.total_dinar += self.price_in_dinar
#                 self.container.total_dollar += self.price_in_dollar
#                 self.company_name.total_dinar += self.price_in_dinar
#                 self.company_name.total_dollar += self.price_in_dollar
#
#             else:
#                 if old_price_in_dollar > self.price_in_dollar:
#                     temp_price_dollar = old_price_in_dollar - self.price_in_dollar
#                     self.container.total_dollar -= temp_price_dollar
#                     self.company_name.total_dollar -= temp_price_dollar
#
#                 elif old_price_in_dollar < self.price_in_dollar:
#                     temp_price_dollar = self.price_in_dollar - old_price_in_dollar
#                     self.container.total_dollar += temp_price_dollar
#                     self.company_name.total_dollar += temp_price_dollar
#
#                 if old_price_in_dinar > self.price_in_dinar:
#                     temp_price_dinar = old_price_in_dinar - self.price_in_dinar
#                     self.container.total_dinar -= temp_price_dinar
#                     self.company_name.total_dinar -= temp_price_dinar
#
#                 elif old_price_in_dinar < self.price_in_dinar:
#                     temp_price_dinar = self.price_in_dinar - old_price_in_dinar
#                     self.container.total_dinar += temp_price_dinar
#                     self.company_name.total_dinar += temp_price_dinar
#
#             # Save the updated data
#             self.container.save()
#             self.company_name.save()
#             super().save(*args, **kwargs)
#
#     def delete(self, using=None, keep_parents=False):
#         with transaction.atomic():
#             if self.container:
#                 self.container.total_dinar -= self.price_in_dinar
#                 self.container.total_dollar -= self.price_in_dollar
#                 self.company_name.total_dinar -= self.price_in_dinar
#                 self.company_name.total_dollar -= self.price_in_dollar
#
#                 # Save the updated Container
#                 self.container.save()
#                 self.company_name.save()
#             super().delete(using=using, keep_parents=keep_parents)
#
#
# class Withdraw(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice_id = models.CharField(max_length=10, unique=True, editable=False)
#     withdraw_type = models.ForeignKey(WithdrawType, on_delete=models.PROTECT)
#     container = models.ForeignKey(Container, on_delete=models.CASCADE)
#     company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
#     price_in_dinar = models.FloatField()
#     price_in_dollar = models.FloatField()
#     description = models.TextField(max_length=2000)
#     out_to = models.CharField(max_length=255)
#     created_at = models.DateTimeField()
#     record_created_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#                                    related_name='created_by_withdrawer')
#     withdraw_number = models.PositiveIntegerField(
#         blank=True, unique=True)  # New field
#     document = models.FileField(
#         upload_to='withdraw_documents/', blank=True, null=True)
#
#     def __str__(self):
#         return self.invoice_id
#
#     class Meta:
#         verbose_name_plural = 'الصرفيات'
#
#     def generate_invoice_id(self):
#         # Customize the prefix or length as needed
#         prefix = "INV"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:6]
#         return f"{prefix}-{unique_id}"
#
#     def save(self, *args, **kwargs):
#
#         old_price_in_dinar = 0
#         old_price_in_dollar = 0
#         # Retrieve the existing data before update
#         try:
#             old_instance = Withdraw.objects.get(pk=self.pk)
#             old_price_in_dinar = old_instance.price_in_dinar
#             old_price_in_dollar = old_instance.price_in_dollar
#         except Withdraw.DoesNotExist:
#             # If the instance does not exist yet, set old_instance to None
#             old_instance = None
#
#         if not self.withdraw_number:  # Only generate deposit_number if not set
#             last_withdraw = Withdraw.objects.order_by(
#                 '-withdraw_number').first()
#             if last_withdraw:
#                 self.withdraw_number = last_withdraw.withdraw_number + 1
#             else:
#                 self.withdraw_number = 1
#
#         with transaction.atomic():
#             if not self.invoice_id:
#                 # Generate a short and secure invoice ID
#                 self.invoice_id = self.generate_invoice_id()
#
#                 self.container.total_dinar -= self.price_in_dinar
#                 self.container.total_dollar -= self.price_in_dollar
#                 self.company_name.total_dinar -= self.price_in_dinar
#                 self.company_name.total_dollar -= self.price_in_dollar
#                 # Save the updated Container
#                 self.container.save()
#                 self.company_name.save()
#             else:
#                 if old_price_in_dollar > self.price_in_dollar:
#                     temp_price_dollar = old_price_in_dollar - self.price_in_dollar
#                     self.container.total_dollar += temp_price_dollar
#                     self.company_name.total_dollar += temp_price_dollar
#                 elif old_price_in_dollar < self.price_in_dollar:
#                     temp_price_dollar = self.price_in_dollar - old_price_in_dollar
#                     self.container.total_dollar -= temp_price_dollar
#                     self.company_name.total_dollar -= temp_price_dollar
#
#                 if old_price_in_dinar > self.price_in_dinar:
#                     temp_price_dinar = old_price_in_dinar - self.price_in_dinar
#                     self.container.total_dinar += temp_price_dinar
#                     self.company_name.total_dinar += temp_price_dinar
#
#                 elif old_price_in_dinar < self.price_in_dinar:
#                     temp_price_dinar = self.price_in_dinar - old_price_in_dinar
#                     self.container.total_dinar -= temp_price_dinar
#                     self.company_name.total_dinar -= temp_price_dinar
#
#             # Save the updated data
#             self.container.save()
#             self.company_name.save()
#             super().save(*args, **kwargs)
#
#     def delete(self, using=None, keep_parents=False):
#         with transaction.atomic():
#             if self.container:
#                 self.container.total_dinar += self.price_in_dinar
#                 self.container.total_dollar += self.price_in_dollar
#                 self.company_name.total_dinar += self.price_in_dinar
#                 self.company_name.total_dollar += self.price_in_dollar
#
#                 # Save the updated Container
#                 self.container.save()
#                 self.company_name.save()
#             super().delete(using=using, keep_parents=keep_parents)
#
#
# class Invoice(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice_id = models.CharField(max_length=10, unique=True, editable=False)
#     title = models.CharField(max_length=255)
#     description = models.JSONField()
#     created_at = models.DateTimeField(auto_now=True)
#
#     def generate_invoice_id(self):
#         # Customize the prefix or length as needed
#         prefix = "#"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:6]
#         return f"{prefix}{unique_id}"
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if not self.invoice_id:
#                 # Generate a short and secure invoice ID
#                 self.invoice_id = self.generate_invoice_id()
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'الفواتير'
#
#
# class BuildingCalc(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice_id = models.CharField(max_length=10, unique=True, editable=False)
#     title = models.CharField(max_length=255)
#     description = models.JSONField()
#     created_at = models.DateTimeField(auto_now=True)
#
#     def generate_invoice_id(self):
#         # Customize the prefix or length as needed
#         prefix = "#"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:6]
#         return f"{prefix}{unique_id}"
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if not self.invoice_id:
#                 # Generate a short and secure invoice ID
#                 self.invoice_id = self.generate_invoice_id()
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'ذرعات البنايات'
#
#
# class WorkerCalc(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice_id = models.CharField(max_length=10, unique=True, editable=False)
#     title = models.CharField(max_length=255)
#     description = models.JSONField()
#     created_at = models.DateTimeField(auto_now=True)
#
#     def generate_invoice_id(self):
#         # Customize the prefix or length as needed
#         prefix = "#"
#         # Extract 6 characters from the UUID
#         unique_id = str(uuid.uuid4().int)[:6]
#         return f"{prefix}{unique_id}"
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if not self.invoice_id:
#                 # Generate a short and secure invoice ID
#                 self.invoice_id = self.generate_invoice_id()
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name_plural = 'ذرعات الخلفات'
#
# # class EndpointLog(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL,
# #                              on_delete=models.SET_NULL,
# #                              null=True, blank=True, related_name="log_user")
# #     path = models.CharField(max_length=200)
# #     action = models.CharField(max_length=50, blank=True, null=True)  # New field for action
# #     method = models.CharField(max_length=10)
# #     status_code = models.IntegerField()
# #     timestamp = models.DateTimeField(auto_now_add=True)
# #
# #     def __str__(self):
# #         return f"{self.method} {self.path} {self.status_code}"
#
# # class LogEntry(models.Model):
# #     timestamp = models.DateTimeField(auto_now_add=True)
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL,
# #                              on_delete=models.SET_NULL,
# #                              null=True, blank=True, related_name="log_user")
# #     action = models.CharField(max_length=255)
# #     details = models.TextField()
# #     model_affected = models.CharField(max_length=100, null=True, blank=True)
# #     record_id = models.PositiveIntegerField(null=True, blank=True)
# #
# #     def __str__(self):
# #         return f"{self.timestamp} - {self.user} - {self.action}"
