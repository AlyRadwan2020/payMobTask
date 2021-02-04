import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from task.models import NormalUser, AdminUser, Promo

# create_promo test
from task.serializers import PromoSerializer


class PromoCreationTestCase(APITestCase):

    def setUp(self):
        # Promo.objects.create()
        self.client = Client()
        # create  user
        self.user = get_user_model().objects.create_superuser(
            "admintest",
            "admintest@paymob.com",
            "admintest"
        )
        # create AdminUser
        self.adminUser = AdminUser.objects.create(user=self.user, name="adminUser", address="plu pl o o jk ")

        # create Normal user1
        self.user1 = get_user_model().objects.create_superuser(
            "normaluser1",
            "normaluser1@paymob.com",
            "normaluser1"
        )
        self.normalUser1 = NormalUser.objects.create(user=self.user1, mobile_number='0123456789', name="normaluser1",
                                                     address="plu pl o o jk ")

        # create Normal user2
        self.user2 = get_user_model().objects.create_superuser(
            "normaluser2",
            "normaluser2@paymob.com",
            "normaluser2"
        )
        self.normalUser2 = NormalUser.objects.create(user=self.user2, mobile_number='0123456789', name="normaluser2",
                                                     address="plu pl o o jk ")

        # create promotion object with id=1
        Promo.objects.create(id=1, normal_user=self.normalUser1, promo_type="type_1", promo_code='Test1',
                             start_time=datetime.now() + timedelta(days=1),
                             end_time=datetime.now() + timedelta(days=3), promo_amount=100, is_active=True,
                             description="")

        # create promotion object with id=2
        Promo.objects.create(id=2, normal_user=self.normalUser2, promo_type="type_2", promo_code='Test2',
                             start_time=datetime.now() + timedelta(days=1),
                             end_time=datetime.now() + timedelta(days=3), promo_amount=100, is_active=True,
                             description="")

    def test_promotion_creation_by_admin(self):
        self.client.login(username='admintest', password='admintest')
        data = {
            "promo_amount": 90,
            "promo_type": "type_1",
            "promo_code": "CCe3w",
            "start_time": "2021-02-04T14:46:00Z",
            "end_time": "2021-02-11T14:46:00Z",
            "is_active": False,
            "description": "any description",
            "normal_user": 1
        }
        response = self.client.post('/promos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_promotions_list_by_admin(self):
        self.client.login(username='admintest', password='admintest')
        response = self.client.get('/promos/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_promotions_update_by_admin(self):
        self.client.login(username='admintest', password='admintest')
        promo = Promo.objects.get(id=1)
        data = {
            "promo_amount": 50,
            "promo_type": "type_1",
            "promo_code": "CCe3w",
            "start_time": "2021-02-04T14:46:00Z",
            "end_time": "2021-02-11T14:46:00Z",
            "is_active": False,
            "description": "any description",
            "normal_user": promo.normal_user_id
        }
        response = self.client.put('/promos/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_promotions_delete_by_admin(self):
        self.client.login(username='admintest', password='admintest')
        response = self.client.delete('/promos/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_promotions_list_by_normal_user(self):
        self.client.login(username='normaluser1', password='normaluser1')
        userId = NormalUser.objects.get(name='normaluser1').id
        promos = Promo.objects.filter(normal_user__name='normaluser1')
        response = self.client.get('/promos/', format='json')
        responseJson = json.loads(response.content)
        for promo in responseJson:
            self.assertEqual(userId, promo['normal_user'])

    def test_promotion_remaining_points_get_for_normal_user(self):
        self.client.login(username='normaluser1', password='normaluser1')
        response = self.client.get('/promos/1/points', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_promotion_remaining_points_deduct_for_normal_user(self):
        self.client.login(username='normaluser1', password='normaluser1')
        data = {
            "promo_amount": 20
        }
        response = self.client.put('/promos/1/points', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_promotion_remaining_points_deduct_for_normal_user_with_no_permission(self):
        """
        if normal user try to change another user promotion points it returns HTTP_401_UNAUTHORIZED
        :return:
        """
        self.client.login(username='normaluser1', password='normaluser1')
        data = {
            "promo_amount": 20
        }
        response = self.client.put('/promos/2/points', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
