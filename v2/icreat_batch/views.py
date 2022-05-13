from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .cron import batch_get_data

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IcreatBatchView(APIView):
    """
        작성자 : 남기윤
        공공 데이터 포털 조회된 데이터를 DB에 최신화 및 로깅
    """
    @swagger_auto_schema(
        tags=['Batch API'],
        responses={
            201: '성공',
        },
        operation_summary='API 서버로부터 임상 과제들을 갱신합니다.',
        operation_description="""
        질병관리청 임상연구 과제정보로부터 OpenAPI 형식으로
        임상 과제들을 갱신받습니다.
        """,
    )
    def post(self, request):
        batch_get_data()
        return Response({'message' : "success!"}, status=status.HTTP_201_CREATED)
