from django.urls import path
from .views import resize_background_image_view, resize_recreated_background_image_view

urlpatterns = [
    path('api/v1/resize-background-image', resize_background_image_view, name='resize-background-image'),
    path('api/v1/resize-recreated-background-image', resize_recreated_background_image_view, name='resize-recreated-background-image'),
]
