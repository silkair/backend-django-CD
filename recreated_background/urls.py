from django.urls import path
from .views import recreate_background_view, recreated_background_manage


urlpatterns = [
    path('recreated-backgrounds/', recreate_background_view, name='recreated-backgrounds'),
    path('recreated-backgrounds/<int:recreated_backgroundId>', recreated_background_manage, name='recreated-background-manage')
]

