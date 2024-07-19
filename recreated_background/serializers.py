from rest_framework import serializers
from .models import RecreatedBackground

class RecreatedBackgroundSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)
    image_id = serializers.SerializerMethodField(read_only=True)

    def get_user_id(self, obj):
        return obj.background.user.id  # Background 모델의 user ID를 반환합니다.

    def get_image_id(self, obj):
        return obj.background.image.id  # Background 모델의 image ID를 반환합니다.

    class Meta:
        model = RecreatedBackground
        fields = [
            'id',  # RecreatedBackground 객체의 고유 식별자
            'background',  # Background 객체와의 외래 키 관계
            'user_id',  # Background 객체와 연관된 사용자 ID
            'image_id',  # Background 객체와 연관된 이미지 ID
            'image_url',  # 생성된 이미지 URL
        ]
        read_only_fields = [
            'id',
            'background',
            'user_id',
            'image_id',
        ]
