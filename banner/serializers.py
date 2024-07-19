from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_id', 'user_id', 'item_name', 'item_concept', 'item_category', 'add_information']

class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'maintext', 'servetext', 'maintext2', 'servetext2', 'image_id', 'user_id']

class BannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept', 'item_category', 'add_information', 'user_id', 'image_id']
