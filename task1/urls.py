from django.urls import path
from .views import index, get_last_deals, create_deal

urlpatterns = [
    path('', index, name='index'),
    path('get_last_deals/', get_last_deals, name='get_last_deals'),
    path('create_deal/', create_deal, name='create_deal'),
]