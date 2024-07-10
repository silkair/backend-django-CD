#admin.py: 관리자 사이트 -> 모델을 관리자 사이트에 등록해 데이터베이스의 데이터를 조회, 관리
from django.contrib import admin

from background.models import (Background)

# Register your models here.
class BackgroundAdmin(admin.ModelAdmin):
    search_fields = ['gen_type', 'concept_option', 'image_url']

admin.site.register(Background, BackgroundAdmin)