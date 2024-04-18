from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mms_api.apiviews import (VendorAPI, UploadVendorsAsExcel, CreatePaymentAPI,
                              PaymentAPI, PaymentCycleAPI, PaymentMethodAPI,
                              VendorPaymentsSummaryAPI, VendorIdNameAPI,
                              UpdateVendorAPI, VendorByIdAPI,
                              GetVendorUpdatesAPI, CreateVendorUpdateAPI,
                              GetSingleVendorUpdatesAPI,UpdateVendorTableFromBigQueryAPI
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
    path('update_vendors_from_big_query/', UpdateVendorTableFromBigQueryAPI.as_view(), name="update all vendors"),
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

    # login
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
# Configure URL patterns for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
