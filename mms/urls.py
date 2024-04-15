from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mms_api.apiviews import (VendorAPI, UploadVendorsAsExcel, CreatePaymentAPI,
                              PaymentAPI, PaymentCycleAPI, PaymentMethodAPI,
                              VendorPaymentsSummaryAPI, VendorIdNameAPI,
                              UpdateVendorAPI, VendorByIdAPI,
                              GetVendorUpdatesAPI, CreateVendorUpdateAPI,
                              GetSingleVendorUpdatesAPI
                              )
from core.serializers import CustomUserSerializer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from core.apiviews import UsersListAPI
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Assuming you have a serializer for your user model
        user_serializer = CustomUserSerializer(self.user).data
        data.update({'user': user_serializer})
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Admin Site Config
admin.sites.AdminSite.site_header = 'حساباتي'
admin.sites.AdminSite.site_title = 'حساباتي'
admin.sites.AdminSite.index_title = 'حساباتي'

urlpatterns = [
    path('admin/', admin.site.urls),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # mms api
    # all vendors
    path('vendors/', VendorAPI.as_view(), name="all vendors"),
    path('vendor/<int:pk>', VendorByIdAPI.as_view(), name="single vendor"),
    path('create_vendor_update_log/', CreateVendorUpdateAPI.as_view(),
         name="create vendor update"),
    path('vendor_update_logs/', GetVendorUpdatesAPI.as_view(),
         name="get vendor updates log"),
    path('vendor_single_update_logs/<int:pk>', GetSingleVendorUpdatesAPI.as_view(),
         name="get single vendor updates log"),
    path('update_vendor/<int:vendor_id>',
         UpdateVendorAPI.as_view(), name="update vendor"),
    path('payment_cycles/', PaymentCycleAPI.as_view(), name="all cycles"),
    path('payment_methods/', PaymentMethodAPI.as_view(), name="all methods"),
    path('payments/', PaymentAPI.as_view(), name="all Payments"),
    path('create_payment/', CreatePaymentAPI.as_view(),
         name="create new Payments"),
    path('get_vendor_id_name/', VendorIdNameAPI.as_view(),
         name="vendor id name only"),

    path('upload_vendors_as_excel/',
         UploadVendorsAsExcel.as_view(), name="all vendors"),
    # payment summary
    path('vendor-payments-summary/', VendorPaymentsSummaryAPI.as_view(),
         name='vendor-payments-summary'),
    path('account_managers/', UsersListAPI.as_view(), name='account_managers'),

    # path('create_deposit/', DepositCreateAPI.as_view(), name="create deposit"),
    # path('withdraws/', WithdrawAPI.as_view(), name="withdraw"),
    # path('withdraws_report/', WithdrawsReportAPI.as_view(), name="withdraws report"),
    # path('deposits_report/', DepositsReportAPI.as_view(), name="deposits report"),
    # path('create_withdraw/', WithdrawCreateAPI.as_view(), name="create withdraw"),
    # path('withdraw_types/', WithdrawTypeAPI.as_view(), name="fetch all withdraw types"),
    # path('create_withdraw_type/', CreateWithdrawTypeAPI.as_view(), name="create withdraw type"),
    # # building calc apis
    # path('create_building_calc/',BuildingCalcAPI.as_view(),name="create bulding calc"),
    # path('get_all_building_calc/',BuildingCalcAPI.as_view(), name="get all building calc api"),
    #
    # # worker calc apis
    # path('create_worker_calc/', WorkerCalcAPI.as_view(), name="create worker calc"),
    # path('get_all_worker_calc/', WorkerCalcAPI.as_view(), name="get all worker calc"),
    # # invoices
    # path('create_invoice/', InvoiceAPI.as_view(), name="create invoice"),
    # path('invoices/', InvoiceAPI.as_view(), name="get all invoices"),
    # containers
    # path('container_deposits/<uuid:pk>', ContainerDepositAPI.as_view(), name="container deposits"),
    # path('container_withdraws/<uuid:pk>', ContainerWithdrawsAPI.as_view(), name="container withdraws"),
    # # company
    # path('company_deposits/<uuid:pk>', CompanyDepositAPI.as_view(), name="container deposits"),
    # path('company_withdraws/<uuid:pk>', CompanyWithdrawsAPI.as_view(), name="container withdraws"),
    # path('company_supervisor/<int:pk>', CompanySupervisorAPI.as_view(), name="company supervisor"),
    # path('company_type/', CompanyTypeAPI.as_view(), name="fetch all company_type "),
    # path('companies/', CompaniesListAPI.as_view(), name="list companies"),
    # path('company_create/', CompanyCreateAPI.as_view(), name="create company"),
    # login
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
# Configure URL patterns for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
