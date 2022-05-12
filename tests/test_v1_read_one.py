from rest_framework.test import APITestCase
from rest_framework import status

from v1.icreat.serializers import IcreatSerializer
from v1.icreat.models import Icreat

class TestIcreatReadOne(APITestCase):
    """
    작성자: 하정현
    """
    API = '/api/v1/icreat'
    user_id = 0

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
    
    def test_read(self):
        res = self.client.get(f"{self.API}{self.user_id}")
        self.assertEqual(res.status_code, 200)

    def test_read_failed(self):
        # 없는 sub num
        res = self.client.get(f"{self.API}44444")
        self.assertEqual(res.status_code, 404)
