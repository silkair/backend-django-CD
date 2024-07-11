from django.urls import path
from .views import backgrounds_view, background_manage

urlpatterns = [
    path('backgrounds/', backgrounds_view, name='backgrounds'),
    path('backgrounds/<int:background_id>/', background_manage, name='background-manage'),
]
