from rest_framework.test import APITestCase
from rest_framework import status

from apps.icreat.serializers import IcreatSerializer
from apps.icreat.models import Icreat


class TestIcreatCreate(APITestCase):
    """
    작성자 하정현

    시간이 남으면 Serializer 디버깅과 함께 테스트케이스 대폭 강화 예정
    """
    UPLOAD_API = f'/api/icreat'
    
    def test_create_success(self):
        # 데이터 전부 채우고 정상작동 테스트
        req = {
            "subject": "SubJect",
            "sub_num": "C13453",
            "period": "3년",
            "boundary": "국내다기관",
            "remark": "관찰연구",
            "institute": "서울아산병원",
            "trial": "코호트",
            "goal_research": "120",
            "meddept": "Pediatrics",
            "is_active": True,
        }

        res = self.client.post(self.UPLOAD_API, data=req)
        self.assertEqual(res.status_code, 201)

        # 동일 데이터 업로드 불가
        res = self.client.post(self.UPLOAD_API, data=req)
        self.assertEqual(res.status_code, 400)
    
    def test_create_only_requirements(self):
        # 필수 사항만 업로드
        req = {
            "subject": "SubJect",
            "sub_num": "C13453",
            "boundary": "국내다기관",
            "remark": "관찰연구",
            "institute": "서울아산병원",
            "meddept": "Pediatrics",
            "is_active": True,
        }
        res = self.client.post(self.UPLOAD_API, data=req)
        self.assertEqual(res.status_code, 201)


    def test_create_omit_requirements(self):
        # 필수 사항만 업로드
        req = {
            "sub_num": "C13453",
            "boundary": "국내다기관",
            "remark": "관찰연구",
            "institute": "서울아산병원",
            "meddept": "Pediatrics",
            "is_active": True,
        }
        res = self.client.post(self.UPLOAD_API, data=req)
        self.assertEqual(res.status_code, 400)
