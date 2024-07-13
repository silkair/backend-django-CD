from django.urls import path
from .views import resize_background_image_view, resize_recreated_background_image_view, recreated_background_image_manage, background_image_manage

urlpatterns = [
    path('api/v1/resize-background-image', resize_background_image_view, name='resize-background-image'),
    path('api/v1/resize-recreated-background-image', resize_recreated_background_image_view, name='resize-recreated-background-image'),
    path('api/v1/resize-background-image/<int:background_image_id>', background_image_manage, name='background-image-manage'),
    path('api/v1/resize-recreated-background-image/<int:recreated_background_image_id>', recreated_background_image_manage, name='recreated-background-image-manage'),
]
