from rest_framework import serializers
from .models import Background
class BackgroundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Background
        fields = [
            'id', 'user', 'image', 'gen_type', 'concept_option', 'output_h',
            'output_w', 'image_url', 'created_at', 'updated_at', 'is_deleted', 'recreated'
        ]
        read_only_fields = ['id', 'image_url', 'created_at', 'updated_at']