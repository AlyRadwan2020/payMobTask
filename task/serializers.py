from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from task.models import Promo, NormalUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = NormalUser
        # fields = ['username', 'first_name', 'last_name', 'email', ]
        fields = '__all__'


class PromoSerializer(ModelSerializer):
    # user = UserSerializer(many=False)
    promo_amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Promo
        fields = "__all__"


class PromoPointsSerializer(ModelSerializer):
    promo_amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Promo
        fields = ['promo_amount', ]
