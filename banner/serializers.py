from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept']

class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'item_name', 'item_concept', 'ad_text', 'created_at']

class BannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept']
