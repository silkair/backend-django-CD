from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_id', 'user_id', 'item_name', 'item_concept', 'item_category', 'add_information']

class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'ad_text', 'serve_text', 'ad_text2', 'serve_text2', 'image_id', 'user_id']

class BannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept', 'item_category', 'add_information', 'user_id', 'image_id']
