from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from uritemplate import partial
from .serializers import IcreatSerializer
from .models import Icreat
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from v1.icreat.models import Icreat

'''
작성자 : 남기윤, 하정현
'''

class SubjectDetailView(RetrieveUpdateDestroyAPIView):

    # apiview variables
    model = Icreat
    serializer_class = IcreatSerializer
    
    def get_queryset(self):
        res = Icreat.objects.all()
        return res

    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            200: openapi.Response('id에 대한 임상 실험 정보를 불러옵니다.', IcreatSerializer),
            404: '해당 id에 대한 정보를 찾을 수 없음'
        },
        operation_summary='임상 과제의 세부 정보를 가져옵니다.',
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            200: '성공',
            404: '해당 id에 대한 정보를 찾을 수 없음',
            400: '일부 데이터의 포맷이 맞지 않음'
        },
        operation_summary='임상 과제의 정보를 수정합니다.',
    )
    def patch(self, request, pk):
        return self.update(request, pk, partial = True)

    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            200: '성공',
            404: '해당 id에 대한 정보를 찾을 수 없음',
            400: '일부 데이터의 포맷이 맞지 않음'
        },
        operation_summary='임상 과제의 정보를 수정합니다.',
    )
    def put(self, request, pk):
        return self.update(request, pk, partial = True)
    
    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            204: '성공',
            404: '해당 id에 대한 정보를 찾을 수 없음'
        },
        operation_summary='임상 과제의 정보를 삭제합니다.',
    )
    def delete(self, request, pk):
        """
        이때 실제로 Table에서 삭제되는 것이 아닌
        is_active를 False로 지정합니다.
        """
        obj = get_object_or_404(Icreat, id=pk)
        if not obj.is_active:
            # 이미 삭제처리됨
            return Response({"error": "already deleted"}, status=status.HTTP_400_BAD_REQUEST)
        obj.is_active = False
        obj.save()
        return Response({"is_active": obj.is_active}, status=status.HTTP_204_NO_CONTENT)

class SubjectListView(ListCreateAPIView): #/api/v1/icreat/list
    model = Icreat
    serializer_class = IcreatSerializer

    def get_queryset(self):
        page = self.request.GET.get('page',1)
        pagesize = 10
        limit = pagesize * page
        offset = limit -pagesize
        a_week_ago = datetime.today() - timedelta(days = 7)
        subjects = Icreat.objects.filter(modified_at__gte=a_week_ago)[offset:limit]
        return subjects
    
    """
    아래 함수는 SWAGGER 작성을 위해서
    따로 생성
    """
    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            200: openapi.Response(
                description="성공",
                examples={
                    "application/json": {
                        "result": [
                            {
                                "subject": "string",
                                "sub_num": "string",
                                "period": "string",
                                "boundary": "string",
                                "remark": "string",
                                "institute": "string",
                                "trial": "string",
                                "goal_research": "string",
                                "meddept": "string",
                                "is_active": True
                            },
                            {
                                "subject": "string",
                                "sub_num": "string",
                                "period": "string",
                                "boundary": "string",
                                "remark": "string",
                                "institute": "string",
                                "trial": "string",
                                "goal_research": "string",
                                "meddept": "string",
                                "is_active": True
                            }
                        ]
                    }
                }
            )
        },
        operation_summary='최근 일주일 내 변경이 있는 10개의 임상 과제들을 가져옵니다.',
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @swagger_auto_schema(
        tags=['Icreate CRUD'],
        responses={
            201: '성공',
            400: '일부 데이터의 포맷이 맞지 않음',
        },
        operation_summary='새로운 임상 과제를 추가합니다.',
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)