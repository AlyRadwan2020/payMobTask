from django.urls import path, include

from task import promo_views,user_views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('promos/<int:pk>/', promo_views.PromoRUD.as_view(), name='RUD_promo'),
    path('promos/', promo_views.PromoListCreate.as_view(), name='List_create_promos'),
    path('user/<int:pk>/', user_views.UserRUD.as_view(), name='RUD_user'),
    path('users/', user_views.UserListCreate.as_view(), name='List_create_promos'),
    path('promos/<int:pk>/points',promo_views.UserPromoPoints.as_view(),name='Get_promo_points'),
]
