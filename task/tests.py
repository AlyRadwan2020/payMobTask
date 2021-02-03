from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from task.models import NormalUser, AdminUser


# create_promo test
class PromoCreationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # create  user
        self.user = get_user_model().objects.create_superuser(
            "admintest",
            "admintest@admintest.com",
            "admintest"
        )
        # create AdminUser
        self.adminUser = AdminUser.objects.create(user=self.user, name="adminUser", address="plu pl o o jk ")

        self.client.login(username='admintest', password='admintest')

    def normal_user_creation(self):
        self.normaluser_auth = get_user_model().objects.create_superuser(
            "normaluser",
            "normaluser@admintest.com",
            "normaluser"
        )
        # create AdminUser
        normaluser = NormalUser.objects.create(user=self.normaluser_auth, name="normaluser", address="plu pl o o jk ",
                                               mobile_number='0123456789')

        return normaluser

    def test_admin_promotion_creation(self):
        normaluser = self.normal_user_creation()
        data = {
            "promo_amount": 90,
            "promo_type": "type_1",
            "promo_code": "CCe3w",
            "start_time": "2021-02-04T14:46:00Z",
            "end_time": "2021-02-11T14:46:00Z",
            "is_active": False,
            "description": "any description",
            "normal_user": normaluser.id

        }

        response = self.client.post('/promos/', data, format='json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_promotions_list(self):
        response = self.client.get('/promos/', format='json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_promotions_update(self):
        data = {
                    "id": 1,
                    "promo_amount": 80,
                    "promo_type": "type_1",
                    "promo_code": "CCC2",
                    "creation_time": "2021-02-03T12:46:45.157016Z",
                    "start_time": "2021-02-04T14:46:00Z",
                    "end_time": "2021-02-11T14:46:00Z",
                    "is_active": False,
                }
        response = self.client.put('/promos/1/',data ,format='json')
        print("update"+str(response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_modify_promo(self):
    #     data = {
    #         "id": 1,
    #         "promo_amount": 80,
    #         "promo_type": "type_1",
    #         "promo_code": "CCC2",
    #         "creation_time": "2021-02-03T12:46:45.157016Z",
    #         "start_time": "2021-02-04T14:46:00Z",
    #         "end_time": "2021-02-11T14:46:00Z",
    #         "is_active": False,
    #         "description": "",
    #         "normal_user": 1
    #     }
    #     response = self.client.put('/promos/1/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


# class PromoModificationTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # create  user
#         self.user = get_user_model().objects.create_superuser(
#             "admin",
#             "normaluser@admintest.com",
#             "normaluser"
#         )
#         # create AdminUser
#         self.normaluser = AdminUser.objects.create(user=self.user, name="normaluser", address="plu pl o o jk ")
#
#         self.client.login(username='normaluser', password='normaluser')
#     def test_user_modify_promo(self):
#         print('PromoModificationTestCase')
#         data = {
#             "id": 1,
#             "promo_amount": 80,
#             "promo_type": "type_1",
#             "promo_code": "CCC2",
#             "creation_time": "2021-02-03T12:46:45.157016Z",
#             "start_time": "2021-02-04T14:46:00Z",
#             "end_time": "2021-02-11T14:46:00Z",
#             "is_active": False,
#             "description": "",
#             "normal_user": se
#         }
#         response = self.client.put('/promos/1/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
