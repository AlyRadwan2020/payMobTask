from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions

from task.models import User, NormalUser
from task.serializers import UserSerializer


# Retrieve , Update and Destroy APIView
class UserRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NormalUser.objects.all()
    serializer_class = UserSerializer


# List and Create APIView
class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NormalUser.objects.all()
    serializer_class = UserSerializer
