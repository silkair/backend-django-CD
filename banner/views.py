import os
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer, BannerDetailSerializer, BannerUpdateSerializer
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_ad_text(item_name, item_concept, item_category):
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a creative copywriter."},
            {"role": "user", "content": f"'{item_name}' 제품의 광고 문구를 '{item_concept}' 개념으로 '{item_category}' 카테고리에서 한국어로 작성해 주세요."}
        ],
        "max_tokens": 50  # 토큰 크기를 50으로 고정
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_json = response.json()
    ad_text = response_json['choices'][0]['message']['content'].strip()
    return ad_text

@swagger_auto_schema(
    method='post',
    operation_id='배너 생성',
    operation_description='광고 배너를 생성합니다. item_name, item_concept, item_category를 입력해야 합니다.',
    request_body=BannerSerializer,
    responses={
        201: '배너 생성 성공',
        400: '잘못된 요청',
    }
)
@api_view(['POST'])
def create_banner(request):
    serializer = BannerSerializer(data=request.data)
    if serializer.is_valid():
        item_name = serializer.validated_data.get('item_name')
        item_concept = serializer.validated_data.get('item_concept')
        item_category = serializer.validated_data.get('item_category')
        user_id = serializer.validated_data.get('user_id')
        image_id = serializer.validated_data.get('image_id')

        ad_text = generate_ad_text(item_name, item_concept, item_category)

        banner = Banner.objects.create(
            item_name=item_name,
            item_concept=item_concept,
            item_category=item_category,
            ad_text=ad_text,
            user_id=user_id,
            image_id=image_id
        )

        response_data = {
            "code": 201,
            "message": "배너 생성 성공",
            "data": BannerSerializer(banner).data,
            "ad_text": ad_text  # 생성된 광고 문구를 response에 추가
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response({"code": 400, "message": "배너 생성 실패", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_id='배너 조회',
    operation_description='ID를 통해 광고 배너를 조회합니다.',
    responses={
        200: openapi.Response(
            description='배너 조회 성공',
            examples={
                'application/json': {
                    "code": 200,
                    "message": "배너 조회 성공",
                    "data": {
                        "id": 1,
                        "item_name": "에어팟 프로2",
                        "item_concept": "중국산",
                        "item_category": "전자제품",
                        "ad_text": "에어팟 프로2를 소개합니다! 이제 중국산 품질로 만나보세요.",
                        "created_at": "2023-01-01T00:00:00Z"
                    }
                }
            }
        ),
        404: '배너 조회 실패',
    }
)
@swagger_auto_schema(
    method='put',
    operation_id='배너 수정',
    operation_description='ID를 통해 광고 배너를 수정합니다. item_name, item_concept, item_category를 입력해야 합니다.',
    request_body=BannerUpdateSerializer,
    responses={
        200: '배너 수정 성공',
        404: '배너 수정 실패',
    }
)
@swagger_auto_schema(
    method='delete',
    operation_id='배너 삭제',
    operation_description='ID를 통해 광고 배너를 삭제합니다.',
    responses={
        200: '배너 삭제 성공',
        404: '배너 삭제 실패',
    }
)
@api_view(['GET', 'PUT', 'DELETE'])
def handle_banner(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
    except Banner.DoesNotExist:
        return Response({"code": 404, "message": "배너 조회 실패"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BannerDetailSerializer(banner)
        return Response({"code": 200, "message": "배너 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BannerUpdateSerializer(banner, data=request.data)
        if serializer.is_valid():
            item_name = serializer.validated_data.get('item_name')
            item_concept = serializer.validated_data.get('item_concept')
            item_category = serializer.validated_data.get('item_category')
            user_id = serializer.validated_data.get('user_id')
            image_id = serializer.validated_data.get('image_id')

            ad_text = generate_ad_text(item_name, item_concept, item_category)

            banner.item_name = item_name
            banner.item_concept = item_concept
            banner.item_category = item_category
            banner.ad_text = ad_text
            banner.user_id = user_id
            banner.image_id = image_id
            banner.save()

            response_data = {
                "code": 200,
                "message": "배너 수정 성공",
                "data": BannerDetailSerializer(banner).data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"code": 400, "message": "배너 수정 실패", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        banner.delete()
        return Response({"code": 200, "message": "배너 삭제 성공"}, status=status.HTTP_200_OK)

    return Response({"code": 405, "message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
