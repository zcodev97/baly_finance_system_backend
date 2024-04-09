from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.pagination import PageNumberPagination
from .serializers import CustomUserSerializer
from .models import User


class UsersListAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    paginator = PageNumberPagination()
    paginator.page_size = None  # Set page size to None to disable pagination
