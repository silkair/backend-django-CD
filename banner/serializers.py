from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image_id', 'user_id', 'item_name', 'item_concept', 'item_category', 'add_information']  # add_information 추가

class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['item_name', 'item_concept', 'item_category', 'add_information', 'user_id', 'image_id']  # user_id와 image_id 추가
