from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Background, Image, User
from .serializers import BackgroundSerializer
import requests
import io
import uuid
import base64
import boto3
from PIL import Image as PILImage
import json
import logging
from django.conf import settings
import traceback

# 로깅 설정
logger = logging.getLogger(__name__)

GEN_TYPES = ['remove_bg', 'color_bg', 'simple', 'concept']

@swagger_auto_schema(method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'image_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Image ID'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'gen_type': openapi.Schema(type=openapi.TYPE_STRING, description='Generation Type', enum=['remove_bg', 'color_bg', 'simple', 'concept']),
            'multiblob_sod': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Multiblob SOD', default=False),
            'output_w': openapi.Schema(type=openapi.TYPE_INTEGER, description='Output Width', default=1000, minimum=200, maximum=2000),
            'output_h': openapi.Schema(type=openapi.TYPE_INTEGER, description='Output Height', default=1000, minimum=200, maximum=2000),
            'bg_color_hex_code': openapi.Schema(type=openapi.TYPE_STRING, description='Background Color Hex Code', default='#FFFFFF', pattern='^#(?:[0-9a-fA-F]{3}){1,2}$'),
            'concept_option': openapi.Schema(type=openapi.TYPE_OBJECT, description='Concept Option', properties={
                'category': openapi.Schema(type=openapi.TYPE_STRING, description='Category', enum=['cosmetics', 'food', 'clothes', 'person', 'car', 'others']),
                'theme': openapi.Schema(type=openapi.TYPE_STRING, description='Theme'),
                'num_results': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of Results', minimum=1, maximum=4)
            }),
        },
        required=['user_id', 'image_id', 'username', 'gen_type']
    ),
    responses={
        201: openapi.Response('AI 이미지 생성 성공', BackgroundSerializer(many=True)),
        400: 'Bad Request',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def backgrounds_view(request):
    # 요청 데이터에서 필요한 값을 추출
    user_id = request.data.get('user_id')
    image_id = request.data.get('image_id')
    username = request.data.get('username')
    gen_type = request.data.get('gen_type')
    multiblob_sod = request.data.get('multiblob_sod', False)
    output_h = request.data.get('output_h', 1000)
    output_w = request.data.get('output_w', 1000)
    bg_color_hex_code = request.data.get('bg_color_hex_code', '#FFFFFF')
    concept_option = request.data.get('concept_option', {})

    logger.debug("Received request data: %s", request.data)

    # 필수 값이 있는지 확인
    if not (user_id and image_id and username and gen_type):
        logger.debug("Missing required parameters: user_id: %s, image_id: %s, username: %s, gen_type: %s", user_id, image_id, username, gen_type)
        return Response({"error": "user_id, image_id, username, and gen_type are required"}, status=status.HTTP_400_BAD_REQUEST)

    # gen_type 값이 유효한지 확인
    if gen_type not in GEN_TYPES:
        logger.debug("Invalid gen_type: %s", gen_type)
        return Response({"error": f"gen_type is invalid. 가능한 값 : {', '.join(GEN_TYPES)}"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 사용자 객체를 가져옴
        user = User.objects.get(id=user_id)
        logger.debug("Fetched user: %s", user)
    except User.DoesNotExist:
        return Response({"error": "사용자 없음"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # 이미지 객체를 가져옴
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return Response({"error": "이미지 없음"}, status=status.HTTP_404_NOT_FOUND)

    # 이미지 테이블에 있는 사용자가 업로드한 사진의 URL을 다운로드
    image_url = image.image_url
    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_file = io.BytesIO(image_response.content)
        logger.debug("Downloaded image from URL: %s", image_url)
    except requests.RequestException as e:
        logger.error("Failed to download image: %s", e)
        return Response({"error": "Failed to download image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # API 호출 준비
    url = "https://api.draph.art/v1/generate/"
    headers = {'Authorization': f'Bearer {settings.DRAPHART_API_KEY}'}

    # 파일 객체에 파일 이름을 수동으로 추가
    files = {
        'image': ('image.jpg', image_file, 'image/jpeg')
    }

    # 요청 데이터 구성
    data = {
        "username": username,
        "gen_type": gen_type,
        "multiblob_sod": multiblob_sod,
        "output_w": output_w,
        "output_h": output_h,
        "bg_color_hex_code": bg_color_hex_code,
        'concept_option': json.dumps(concept_option),
    }

    # API 호출
    response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code != 200:
        logger.debug("AI 이미지 생성 실패: %s", response.text)
        return Response({"error": "AI 이미지 생성 실패", "details": response.text}, status=status.HTTP_400_BAD_REQUEST)

    response_data = response.content

    try:
        # base64 이미지를 디코딩하고 처리
        image_data = base64.b64decode(response_data)
        image_bytes = io.BytesIO(image_data)
        pil_image = PILImage.open(image_bytes)
        pil_image = pil_image.convert('RGB')
        png_image_bytes = io.BytesIO()
        pil_image.save(png_image_bytes, format='PNG')
        png_image_bytes.seek(0)

        # S3에 업로드
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
        unique_filename = f"{uuid.uuid4()}.png"
        s3.upload_fileobj(png_image_bytes, settings.AWS_STORAGE_BUCKET_NAME, unique_filename, ExtraArgs={'ContentType': 'image/png'})
        s3_url = f"http://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"

    except Exception as e:
        logger.error("Error uploading to S3: %s", e)
        return Response({"error": "Failed to upload image to S3", "details": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Background 모델에 저장
    background_image = Background.objects.create(
        user=user,
        image=image,
        gen_type=gen_type,
        concept_option=concept_option,
        output_w=output_w,
        output_h=output_h,
        image_url=s3_url
    )

    # 성공적으로 저장되었음을 클라이언트에게 반환
    serializer = BackgroundSerializer(background_image)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
