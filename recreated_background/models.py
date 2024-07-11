from django.db import models
from background.models import Background
class RecreatedBackground(models.Model):
    # background 필드는 재생성된 배경을 참조합니다.
    # Background 모델의 인스턴스를 외래 키로 가짐 -> 하지만 user_id와 image_id만 참조하고 나머지는 다 독립적이다!
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    concept_option = models.TextField(default='default_concept')
    image_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    # get_image_id 메서드는 관련된 Background 객체의 유저 ID를 반환!
    def get_user_id(self):
        return self.background.user.id

    # get_image_id 메서드는 관련된 Background 객체의 이미지 ID를 반환!
    def get_image_id(self):
        return self.background.image.id

    # __str__ 메서드는 이 모델의 인스턴스를 문자열로 표현할 때의 형식을 정의
    def __str__(self):
        return f'RecreatedBackground {self.id} for Background {self.background.id}'

