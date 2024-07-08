from django.urls import path
from .views import upload_image, get_image, delete_image

urlpatterns = [
    path('api/v1/images/', upload_image, name='upload-image'),  # 이미지 업로드 엔드포인트
    path('api/v1/images/<int:image_id>/', get_image, name='get-image'),  # 이미지 조회 엔드포인트
    path('api/v1/images/<int:image_id>/delete/', delete_image, name='delete-image'),  # 이미지 삭제 엔드포인트
]
