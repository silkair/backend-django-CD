from django.urls import path
from .views import recreate_background_view

urlpatterns = [
    path('api/v1/recreated-backgrounds', recreate_background_view, name='recreated-backgrounds'),

]
