from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=False,blank=False,max_length=30)
    mobile_number = models.CharField(max_length=30)
    address = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=45)

    def __str__(self):
        return self.name


choices = (('type_1', 'type_1'), ('type_2', 'type_2'))


class Promo(models.Model):
    normal_user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    promo_type = models.CharField(choices=choices, max_length=30)
    promo_code = models.CharField(max_length=30, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    promo_amount = models.IntegerField(validators=[MinValueValidator(Decimal('1'))])
    is_active = models.BooleanField(default=False)
    description = models.CharField(max_length=45,blank=True)
