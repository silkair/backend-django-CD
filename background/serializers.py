from rest_framework import serializers
from .models import Background

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = [
            'id', 'user', 'image_url'
        ]
        read_only_fields = ['id', 'image_url']
