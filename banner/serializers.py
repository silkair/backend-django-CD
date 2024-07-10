from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept', 'item_category', 'image_id', 'user_id']


class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept', 'item_category','image_id', 'user_id']
