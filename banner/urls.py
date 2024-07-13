# urls.py
from django.urls import path
from .views import create_banner, handle_banner, get_task_status

urlpatterns = [
    path('', create_banner, name='create_banner'),
    path('<int:banner_id>/', handle_banner, name='handle_banner'),
    #path('task-status/<str:task_id>/', get_task_status, name='get_task_status'),
]
