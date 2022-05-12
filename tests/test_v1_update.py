from rest_framework.test import APITestCase
from rest_framework import status

from v1.icreat.models import Icreat
from v1.icreat.serializers import IcreatSerializer

class TestIcreatUpdate(APITestCase):
    """
    작성자: 하정현
    """
    API = '/api/v1/icreat'

    req = {
            "subject"       : '조직구증식증 임상연구 네트워크 구축 및 운영(HLH)',
            "sub_num"       : 'C130010',
            "period"        : '3년',
            "boundary"      : '국내다기관',
            "remark"        : '관찰연구',
            "institute"     : '서울아산병원',
            "trial"         : "코호트",
            "goal_research" : "120",
            "meddept"       : 'Pediatrics',
            'is_active'     : True
        }

    def setUp(self):
        # 업로드
        s = IcreatSerializer(data=self.req)
        s.is_valid()
        s.save()
        self.user_id = Icreat.objects.get(sub_num=self.req['sub_num']).id
    
    def test_udpate(self):

        # 데이터 수정하기
        req = self.req.copy()
        res = self.client.patch(f"{self.API}{self.user_id}", data={'period': '10년'})
        self.assertEqual(res.status_code, 200)
        
        # 변경 확인
        c = Icreat.objects.all()[0]
        self.assertEqual(c.period, '10년')

    def test_update_failed(self):
        # 없는 유저
        res = self.client.patch(f"{self.API}134532", data={'period': '10년'})
        self.assertEqual(res.status_code, 404)

    def test_no_is_active(self):
        # is_active 수정 불가
        req = self.req.copy()
        res = self.client.patch(f"{self.API}{self.user_id}", data={'is_active': False})
        self.assertEqual(res.status_code, 400)
