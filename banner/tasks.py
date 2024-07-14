from celery import shared_task
from .models import Banner, UserInteraction
from .serializers import BannerSerializer
from asgiref.sync import async_to_sync

@shared_task
def create_banner_task(data):
    from .views import generate_ad_text, generate_serve_text  # 여기서 임포트!

    serializer = BannerSerializer(data=data)
    if serializer.is_valid():
        item_name = serializer.validated_data.get('item_name')
        item_concept = serializer.validated_data.get('item_concept')
        item_category = serializer.validated_data.get('item_category')
        user_id = serializer.validated_data.get('user_id')
        image_id = serializer.validated_data.get('image_id')
        add_information = serializer.validated_data.get('add_information')

        # 이전 상호작용 기록 가져오기
        interaction_records = UserInteraction.objects.filter(user_id=user_id).order_by('-created_at')
        interaction_data = " ".join(record.interaction_data for record in interaction_records)

        ad_text = async_to_sync(generate_ad_text)(item_name, item_concept, item_category, add_information, interaction_data)
        serve_text = async_to_sync(generate_serve_text)(ad_text, interaction_data)

        banner = Banner.objects.create(
            item_name=item_name,
            item_concept=item_concept,
            item_category=item_category,
            ad_text=ad_text,
            serve_text=serve_text,
            user_id=user_id,
            image_id=image_id,
            add_information=add_information
        )

        # 새로운 상호작용 기록 저장
        UserInteraction.objects.create(user_id=user_id, interaction_data=f"Created banner with ad_text: {ad_text}")

        return BannerSerializer(banner).data, ad_text, serve_text
    else:
        return {"errors": serializer.errors}