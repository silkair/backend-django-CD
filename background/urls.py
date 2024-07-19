from django.urls import path
from .views import backgrounds_view, background_manage

urlpatterns = [
    path('backgrounds/', backgrounds_view, name='backgrounds'),
    path('backgrounds/<int:backgroundId>/', background_manage, name='background-manage'),
]
