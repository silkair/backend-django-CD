# views.py

import os
import httpx
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Banner, UserInteraction
from .serializers import BannerSerializer, BannerDetailSerializer, BannerUpdateSerializer
from django.conf import settings

# OpenAI API 키 설정
openai_api_key = settings.OPENAI_API_KEY
from dotenv import load_dotenv
from django.core.cache import cache
import environ
from asgiref.sync import sync_to_async, async_to_sync

# 환경 변수 로드
env = environ.Env()
environ.Env.read_env()

# OpenAI API 키 설정
openai_api_key = env("OPENAI_API_KEY")

# 로깅 설정
logger = logging.getLogger(__name__)

async def generate_ad_text(item_name, item_concept, item_category, add_information, interaction_data):
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "당신은 창의적인 카피라이터입니다. 각 요청에 대해 일관된 광고 문구를 생성하세요."},
            {"role": "user", "content": f"다음 정보를 바탕으로 '{item_name}' 제품의 광고 문구를 생성해 주세요: "
                                        f"컨셉 - '{item_concept}', 카테고리 - '{item_category}', 추가 정보 - '{add_information}'. "
                                        f"이전에 사용자와의 상호작용: {interaction_data}"}
        ],
        "max_tokens": 50
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            ad_text = response_json['choices'][0]['message']['content'].strip()
            return ad_text
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            raise

async def generate_serve_text(ad_text, interaction_data):
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "당신은 창의적인 카피라이터입니다. 각 요청에 대해 일관된 광고 문구를 생성하세요."},
            {"role": "user", "content": f"다음 메인 광고글을 광고하는 서브 광고글을 작성해 주세요: '{ad_text}'. "
                                        f"이전에 사용자와의 상호작용: {interaction_data}"}
        ],
        "max_tokens": 50
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            serve_text = response_json['choices'][0]['message']['content'].strip()
            return serve_text
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            raise

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

        response_data = {
            "code": 201,
            "message": "배너 생성 성공",
            "data": BannerSerializer(banner).data,
            "ad_text": ad_text,
            "serve_text": serve_text
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
                        "serve_text": "에어팟 프로2 광고를 확인해 보세요!",
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
            add_information = serializer.validated_data.get('add_information')

            # 이전 상호작용 기록 가져오기
            interaction_records = UserInteraction.objects.filter(user_id=user_id).order_by('-created_at')
            interaction_data = " ".join(record.interaction_data for record in interaction_records)

            ad_text = async_to_sync(generate_ad_text)(item_name, item_concept, item_category, add_information, interaction_data)
            serve_text = async_to_sync(generate_serve_text)(ad_text, interaction_data)

            banner.item_name = item_name
            banner.item_concept = item_concept
            banner.item_category = item_category
            banner.ad_text = ad_text
            banner.serve_text = serve_text
            banner.user_id = user_id
            banner.image_id = image_id
            banner.add_information = add_information
            banner.save()

            # 새로운 상호작용 기록 저장
            UserInteraction.objects.create(user_id=user_id, interaction_data=f"Updated banner with ad_text: {ad_text}")

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
