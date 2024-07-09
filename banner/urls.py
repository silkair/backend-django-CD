from django.urls import path
from .views import create_banner, handle_banner

urlpatterns = [
    path('', create_banner, name='create_banner'),  # POST 요청을 통한 배너 생성
    path('<int:banner_id>/', handle_banner, name='handle_banner'),  # GET, PUT, DELETE 요청을 통한 배너 조회, 수정, 삭제
]
