from rest_framework import serializers
from .models import RecreatedBackground
class RecreatedBackgroundSerializer(serializers.ModelSerializer):
    # user_id와 image_id를 Background 모델에서 가져오기 위해 SerializerMethodField를 사용합니다.
    user_id = serializers.SerializerMethodField(read_only=True)
    image_id = serializers.SerializerMethodField(read_only=True)

    # user_id를 가져오는 메서드
    def get_user_id(self, obj):
        return obj.get_user_id()

    # image_id를 가져오는 메서드
    def get_image_id(self, obj):
        return obj.get_image_id()

    class Meta:
        model = RecreatedBackground

        fields = [
            'id',  # RecreatedBackground 객체의 고유 식별자
            'background',  # Background 객체와의 외래 키 관계
            'user_id',  # Background 객체와 연관된 사용자 ID
            'image_id',  # Background 객체와 연관된 이미지 ID
            'concept_option',
            'image_url',
            'created_at',
            'updated_at',
            'is_deleted',
        ]

        read_only_fields = [
            'id',
            'background',
            'user_id',
            'image_id',
            'created_at',
            'updated_at'
        ]