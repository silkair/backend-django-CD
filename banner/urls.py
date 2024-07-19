# urls.py
from django.urls import path
from .views import create_banner, handle_banner

urlpatterns = [
    path('', create_banner, name='create_banner'),
    path('<int:banner_id>/', handle_banner, name='handle_banner'),
]
