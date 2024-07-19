from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from background.models import Background
from recreated_background.models import RecreatedBackground
from .models import ImageResizing
from .serializers import BackgroundImageResizingSerializer, RecreatedBackgroundImageResizingSerializer
import requests
import io
import uuid
import boto3
from PIL import Image as PILImage
from django.conf import settings
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# 배경 이미지를 리사이징하는 API 엔드포인트
@swagger_auto_schema(
    method='post',
    operation_id='이미지 리사이징 - 배경 이미지',
    operation_description='가로/세로 길이를 입력받아 배경 이미지를 리사이징합니다.',
    tags=['Resizing'],
    request_body=BackgroundImageResizingSerializer,
    responses={
        200: openapi.Response('리사이징된 이미지 URL 및 ID 반환', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'resized_image_url': openapi.Schema(type=openapi.TYPE_STRING, description='리사이징된 이미지 URL'),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='리사이징된 이미지 ID')
            }
        )),
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def resize_background_image_view(request):
    serializer = BackgroundImageResizingSerializer(data=request.data)
    if serializer.is_valid():
        width = serializer.validated_data.get('width')
        height = serializer.validated_data.get('height')
        background_id = serializer.validated_data.get('background_id')

        # 배경 이미지 객체를 가져옴
        background = get_object_or_404(Background, id=background_id)
        image_url = background.image_url

        try:
            # 이미지를 다운로드
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_file = io.BytesIO(image_response.content)
            pil_image = PILImage.open(image_file)

            # 이미지 리사이징
            pil_image = pil_image.resize((width, height))
            resized_image_bytes = io.BytesIO()
            pil_image.save(resized_image_bytes, format='PNG')
            resized_image_bytes.seek(0)

            # S3에 업로드
            s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
            unique_filename = f"{uuid.uuid4()}.png"
            s3.upload_fileobj(resized_image_bytes, settings.AWS_STORAGE_BUCKET_NAME, unique_filename,
                              ExtraArgs={'ContentType': 'image/png'})
            resized_image_url = f"http://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"

            # ImageResizing 객체 생성 및 저장
            image_resizing = ImageResizing.objects.create(
                background=background,
                width=width,
                height=height,
                image_url=resized_image_url
            )

            return Response({"resized_image_url": resized_image_url, "id": image_resizing.id},
                            status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error("Failed to download image: %s", e)
            return Response({"error": "Failed to download image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("Failed to resize image: %s", e)
            return Response({"error": "Failed to resize image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 재생성된 배경 이미지를 리사이징하는 API 엔드포인트
@swagger_auto_schema(
    method='post',
    operation_id='이미지 리사이징 - 재생성된 배경 이미지',
    operation_description='가로/세로 길이를 입력받아 재생성된 배경 이미지를 리사이징합니다.',
    tags=['Resizing'],
    request_body=RecreatedBackgroundImageResizingSerializer,
    responses={
        200: openapi.Response('리사이징된 이미지 URL 및 ID 반환', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'resized_image_url': openapi.Schema(type=openapi.TYPE_STRING, description='리사이징된 이미지 URL'),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='리사이징된 이미지 ID')
            }
        )),
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def resize_recreated_background_image_view(request):
    serializer = RecreatedBackgroundImageResizingSerializer(data=request.data)
    if serializer.is_valid():
        width = serializer.validated_data.get('width')
        height = serializer.validated_data.get('height')
        recreated_background_id = serializer.validated_data.get('recreated_background_id')

        # 재생성된 배경 이미지 객체를 가져옴
        recreated_background = get_object_or_404(RecreatedBackground, id=recreated_background_id)
        image_url = recreated_background.image_url

        try:
            # 이미지를 다운로드
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_file = io.BytesIO(image_response.content)
            pil_image = PILImage.open(image_file)

            # 이미지 리사이징
            pil_image = pil_image.resize((width, height))
            resized_image_bytes = io.BytesIO()
            pil_image.save(resized_image_bytes, format='PNG')
            resized_image_bytes.seek(0)

            # S3에 업로드
            s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
            unique_filename = f"{uuid.uuid4()}.png"
            s3.upload_fileobj(resized_image_bytes, settings.AWS_STORAGE_BUCKET_NAME, unique_filename,
                              ExtraArgs={'ContentType': 'image/png'})
            resized_image_url = f"http://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"

            # ImageResizing 객체 생성 및 저장
            image_resizing = ImageResizing.objects.create(
                recreated_background=recreated_background,
                width=width,
                height=height,
                image_url=resized_image_url
            )

            return Response({"resized_image_url": resized_image_url, "id": image_resizing.id},
                            status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error("Failed to download image: %s", e)
            return Response({"error": "Failed to download image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("Failed to resize image: %s", e)
            return Response({"error": "Failed to resize image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 생성된 이미지 리사이징 조회 및 삭제 API 엔드포인트
@swagger_auto_schema(
    method='get',
    operation_id='생성된 이미지 리사이징 조회',
    operation_description='생성된 이미지를 리사이징한 결과를 조회합니다.',
    tags=['Resizing'],
    responses={
        200: BackgroundImageResizingSerializer,
        404: "Image not found.",
    }
)
@swagger_auto_schema(
    method='delete',
    operation_id='생성된 이미지 리사이징 삭제',
    operation_description='생성된 이미지를 리사이징한 결과를 삭제합니다.',
    tags=['Resizing'],
    responses={
        200: openapi.Response("Image deleted successfully."),
        404: "Image not found.",
    }
)
@api_view(['GET', 'DELETE'])
def background_image_manage(request, resizing_id):
    try:
        # 이미지 리사이징 객체를 가져옴
        image_resizing = ImageResizing.objects.get(id=resizing_id)
    except ImageResizing.DoesNotExist:
        return Response({"error": "해당 이미지가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # 이미지 리사이징 객체를 직렬화하여 반환
        serializer = BackgroundImageResizingSerializer(image_resizing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
        file_key = image_resizing.image_url.split('/')[-1]
        try:
            # S3에서 파일 삭제
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        except Exception as e:
            logger.error("S3 파일 삭제 오류: %s", e)
            return Response({"error": "S3 파일 삭제 오류", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 이미지 리사이징 객체 삭제
        image_resizing.delete()
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_200_OK)


# 재생성된 이미지 리사이징 조회 및 삭제 API 엔드포인트
@swagger_auto_schema(
    method='get',
    operation_id='재생성 이미지 리사이징 조회',
    operation_description='재생성되어 리사이징을 거친 사진을 조회합니다.',
    tags=['Resizing'],
    responses={
        200: RecreatedBackgroundImageResizingSerializer,
        404: "Image not found.",
    }
)
@swagger_auto_schema(
    method='delete',
    operation_id='재생성 이미지 리사이징 삭제',
    operation_description='재생성되어 리사이징을 거친 사진을 삭제합니다.',
    tags=['Resizing'],
    responses={
        200: openapi.Response("Image deleted successfully."),
        404: "Image not found.",
    }
)
@api_view(['GET', 'DELETE'])
def recreated_background_image_manage(request, recreated_background_image_id):
    try:
        # 이미지 리사이징 객체를 가져옴
        image_resizing = ImageResizing.objects.get(id=recreated_background_image_id)
    except ImageResizing.DoesNotExist:
        return Response({"error": "해당 이미지가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # 이미지 리사이징 객체를 직렬화하여 반환
        serializer = RecreatedBackgroundImageResizingSerializer(image_resizing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
        file_key = image_resizing.image_url.split('/')[-1]
        try:
            # S3에서 파일 삭제
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        except Exception as e:
            logger.error("S3 파일 삭제 오류: %s", e)
            return Response({"error": "S3 파일 삭제 오류", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 이미지 리사이징 객체 삭제
        image_resizing.delete()
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_200_OK)
