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

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    operation_id='이미지 리사이징 - 배경 이미지',
    operation_description='가로/세로 길이를 입력받아 배경 이미지를 리사이징합니다.',
    tags=['Image Resize'],
    request_body=BackgroundImageResizingSerializer,
    responses={
        200: openapi.Response('리사이징된 이미지 URL 반환', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'resized_image_url': openapi.Schema(type=openapi.TYPE_STRING, description='리사이징된 이미지 URL')
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

        background = get_object_or_404(Background, id=background_id)
        image_url = background.image_url

        try:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_file = io.BytesIO(image_response.content)
            pil_image = PILImage.open(image_file)
            pil_image = pil_image.resize((width, height))
            resized_image_bytes = io.BytesIO()
            pil_image.save(resized_image_bytes, format='PNG')
            resized_image_bytes.seek(0)

            s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
            unique_filename = f"{uuid.uuid4()}.png"
            s3.upload_fileobj(resized_image_bytes, settings.AWS_STORAGE_BUCKET_NAME, unique_filename, ExtraArgs={'ContentType': 'image/png'})
            resized_image_url = f"http://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"

            ImageResizing.objects.create(
                background=background,
                width=width,
                height=height,
                image_url=resized_image_url
            )

            return Response({"resized_image_url": resized_image_url}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error("Failed to download image: %s", e)
            return Response({"error": "Failed to download image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("Failed to resize image: %s", e)
            return Response({"error": "Failed to resize image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_id='이미지 리사이징 - 재생성된 배경 이미지',
    operation_description='가로/세로 길이를 입력받아 재생성된 배경 이미지를 리사이징합니다.',
    tags=['Image Resize'],
    request_body=RecreatedBackgroundImageResizingSerializer,
    responses={
        200: openapi.Response('리사이징된 이미지 URL 반환', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'resized_image_url': openapi.Schema(type=openapi.TYPE_STRING, description='리사이징된 이미지 URL')
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

        recreated_background = get_object_or_404(RecreatedBackground, id=recreated_background_id)
        image_url = recreated_background.image_url

        try:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_file = io.BytesIO(image_response.content)
            pil_image = PILImage.open(image_file)
            pil_image = pil_image.resize((width, height))
            resized_image_bytes = io.BytesIO()
            pil_image.save(resized_image_bytes, format='PNG')
            resized_image_bytes.seek(0)

            s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
            unique_filename = f"{uuid.uuid4()}.png"
            s3.upload_fileobj(resized_image_bytes, settings.AWS_STORAGE_BUCKET_NAME, unique_filename, ExtraArgs={'ContentType': 'image/png'})
            resized_image_url = f"http://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"

            ImageResizing.objects.create(
                recreated_background=recreated_background,
                width=width,
                height=height,
                image_url=resized_image_url
            )

            return Response({"resized_image_url": resized_image_url}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error("Failed to download image: %s", e)
            return Response({"error": "Failed to download image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("Failed to resize image: %s", e)
            return Response({"error": "Failed to resize image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)