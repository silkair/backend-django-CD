from django.urls import path
from .views import create_banner, get_banner, update_banner, delete_banner

urlpatterns = [
    path('', create_banner),
    path('<int:banner_id>/', get_banner),
    path('<int:banner_id>/update/', update_banner),

    path('<int:banner_id>/delete/', delete_banner),
]
