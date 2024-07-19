from django.db import models
from user.models import User
from image.models import Image

class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, db_column='image_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    item_name = models.CharField(max_length=10)
    item_concept = models.CharField(max_length=15)
    item_category = models.CharField(max_length=10)

    maintext = models.CharField(max_length=150)  # 메인 광고글 길이 늘림
    servetext = models.CharField(max_length=100, default='Default serve text')  # 기본 값 추가

    maintext2 = models.CharField(max_length=150, blank=True, null=True)  # 새롭게 추가한 maintext2
    servetext2 = models.CharField(max_length=100, blank=True, null=True) # 새롭게 추가한 servetext2

    add_information = models.TextField(null=True, blank=True)  # 추가 정보 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class UserInteraction(models.Model):
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    interaction_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
