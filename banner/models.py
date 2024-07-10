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
    ad_text = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

