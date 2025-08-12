from django.urls import path
from .views import index, get_last_deals

urlpatterns = [
    path('', index, name='index'),
    path('get_last_deals/', get_last_deals, name='get_last_deals'),
]