from django.db import models
from background.models import Background
from recreated_background.models import RecreatedBackground

class ImageResizing(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True, blank=True)
    recreated_background = models.ForeignKey(RecreatedBackground, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_background_id(self):
        return self.background.id if self.background else None

    def get_recreated_background_id(self):
        return self.recreated_background.id if self.recreated_background else None

    def __str__(self):
        return f"ImageResizing {self.id} for Background {self.background} or RecreatedBackground {self.recreated_background}"
