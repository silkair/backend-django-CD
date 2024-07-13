from rest_framework import serializers
from .models import ImageResizing

class BackgroundImageResizingSerializer(serializers.ModelSerializer):
    background_id = serializers.IntegerField()

    class Meta:
        model = ImageResizing
        fields = ['width', 'height', 'background_id', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['image_url', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image_url'] = instance.image_url
        return representation

class RecreatedBackgroundImageResizingSerializer(serializers.ModelSerializer):
    recreated_background_id = serializers.IntegerField()

    class Meta:
        model = ImageResizing
        fields = ['width', 'height', 'recreated_background_id', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['image_url', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image_url'] = instance.image_url
        return representation
