from django.urls import path
from .views import backgrounds_view

urlpatterns = [
    path('backgrounds/', backgrounds_view, name='backgrounds'),
]
