from django.db import models

class Banner(models.Model):
    item_name = models.CharField(max_length=100)
    item_concept = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ad_text = models.TextField(blank=True)
