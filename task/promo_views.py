from django.http import HttpResponse

from rest_framework import generics, permissions

from task.models import Promo, AdminUser, NormalUser
from task.serializers import PromoSerializer, PromoPointsSerializer


# List and Create APIView
def check_object_user_premission(user, objId):
    if AdminUser.objects.filter(user=user).exists():
        return True
    else:
        if Promo.objects.filter(id=objId, normal_user__user=user).exists():
            return True
        else:
            return False


# Let admin user to create promo code for user and disallow normal user
class PromoRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    # Disallow normal user to create promo
    def patch(self, request, *args, **kwargs):
        if NormalUser.objects.filter(user=self.request.user).exists():
            return HttpResponse('Unauthorized', status=401)
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        print(user)
        if AdminUser.objects.filter(user=user).exists():
            return Promo.objects.all()
        elif NormalUser.objects.filter(user=user).exists():
            return Promo.objects.filter(normal_user__user=user)
        else:
            return Promo.objects.none()


# List and Create APIView .
class PromoListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    # override queryset to disallow normal user to access another user promo
    def get_queryset(self):
        user = self.request.user
        if AdminUser.objects.filter(user=user).exists():
            return Promo.objects.all()
        elif NormalUser.objects.filter(user=user).exists():
            return Promo.objects.filter(normal_user__user=user)
        else:
            return Promo.objects.none()


# Check if normal user try to increase his promo points .
def check_object_user_increase_points(new_amount, obj):
    if Promo.objects.get(id=obj).promo_amount > new_amount:
        return True
    else:
        return False


# Let user get and update promo points , only admin and promo user can change points .
class UserPromoPoints(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Promo.objects.all()
    serializer_class = PromoPointsSerializer

    def put(self, request, *args, **kwargs):
        if not check_object_user_premission(self.request.user, kwargs['pk']):
            return HttpResponse('Unauthorized', status=401)
        data = request.data
        if not check_object_user_increase_points(data['promo_amount'], kwargs['pk']):
            return HttpResponse('Unauthorized', status=401)

        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if AdminUser.objects.filter(user=user).exists():
            return Promo.objects.all()
        elif NormalUser.objects.filter(user=user).exists():
            return Promo.objects.filter(normal_user__user=user)
        else:
            return Promo.objects.none()
