from django.urls import path
from .views import resize_background_image_view, resize_recreated_background_image_view, background_image_manage, recreated_background_image_manage

urlpatterns = [
    path('resizings/', resize_background_image_view, name='resize-background-image'),
    path('resizings-recreated/', resize_recreated_background_image_view, name='resize-recreated-background-image'),
    path('resizings/<int:background_image_id>/', background_image_manage, name='background-image-manage'),
    path('resizings-recreated/<int:recreated_background_image_id>/', recreated_background_image_manage, name='recreated-background-image-manage'),
]
