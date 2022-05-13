from datetime import datetime

from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..icreat.models import Icreat
from .utils import get_data
from .models import BatchLog

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IcreatBatchView(APIView):
    """
        작성자 : 최승리
        공공 데이터 포털 조회된 데이터를 DB에 최신화 및 로깅
    """
    def set_col_name(self, after_data):
        # 조회한 공공 데이터의 컬럼명을 Model과 매칭"
        before_data = {
                "subject" : after_data["과제명"],
                "sub_num" : after_data["과제번호"],
                "period" : after_data["연구기간"],
                "boundary" : after_data["연구범위"],
                "remark" : after_data["연구종류"],
                "institute" : after_data["연구책임기관"],
                "trial" : after_data["임상시험단계(연구모형)"],
                "goal_research" : after_data["전체목표연구대상자수"],
                "meddept" : after_data["진료과"]
                }
        return before_data

    def set_batch_log(self, start_time, end_time, created_count, updated_count, created_list, updated_list):
        # 로그 테이블에 값 추가
        BatchLog.objects.create(
            start_time = start_time,
            end_time = end_time,
            created_count = created_count,
            updated_count = updated_count,
            created_list = created_list,
            updated_list = updated_list,
            )

    @swagger_auto_schema(
        tags=['Batch API'],
        responses={
            201: '성공',
        },
        operation_summary='API 서버로부터 임상 과제들을 갱신합니다.',
        operation_description="""
        질병관리청 임상연구 과제정보로부터 OpenAPI 형식으로
        임상 과제들을 갱신받습니다.
        """
    )
    def post(self, request):
        # 로깅을 위한 변수 SET
        created_count = 0
        updated_count = 0
        created_list = [] # 생성된 sub_num list
        updated_list = [] # 업데이트된 sub_num list

        start_time = datetime.now()

        batch_data = get_data() # open api로부터 데이터 조회(.utils.py)
        for data in batch_data['data']:
            set_col_name_data = self.set_col_name(data)
            try:
                create_data = Icreat.objects.create(**set_col_name_data)
                created_list.append(create_data.sub_num)
                created_count += 1
            except IntegrityError: # sub_num은 unique값이므로 중복 생성은 에러발생.
                exist_data = Icreat.objects.filter(sub_num=data["과제번호"]).values(*set_col_name_data.keys())
                if exist_data[0] == set_col_name_data:
                    continue
                else:
                    # 기존에 데이터는 존재하지만 일부 수정이 생겼을 경우 UPDATE
                    exist_data.update(**set_col_name_data, modified_at = datetime.now())
                    updated_count += 1
                    updated_list.append(exist_data[0]['sub_num'])

        end_time = datetime.now()
        # 로그 테이블에 데이터 SET
        self.set_batch_log(start_time, end_time, created_count, updated_count, created_list, updated_list)
        return Response({'message' : "success!"}, status=status.HTTP_201_CREATED)
