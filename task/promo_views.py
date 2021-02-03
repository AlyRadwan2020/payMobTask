from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions

from task.models import Promo, AdminUser, NormalUser
from task.serializers import PromoSerializer, PromoPointsSerializer


# Retrieve , Update and Destroy APIView
class PromoRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


# List and Create APIView
class PromoListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    def get_queryset(self):
        user = self.request.user
        print(user.is_superuser)
        if AdminUser.objects.filter(user=user).exists():
            return Promo.objects.all()
        elif NormalUser.objects.filter(user=user).exists():
            return Promo.objects.filter(normal_user__user=user)
        else:
            return Promo.objects.none()


# List and Create APIView
class UserPromoPoints(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Promo.objects.all()
    serializer_class = PromoPointsSerializer

    def get_queryset(self):
        user = self.request.user
        if AdminUser.objects.filter(user=user).exists():
            return Promo.objects.all()
        elif NormalUser.objects.filter(user=user).exists():
            return Promo.objects.filter(normal_user__user=user)
        else:
            return Promo.objects.none()

