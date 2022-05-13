from rest_framework.test import APITestCase

from apps.icreat.serializers import IcreatSerializer
from apps.icreat.models import Icreat


class TestIcreatDelete(APITestCase):
    """
    작성자: 하정현
    """
    API = '/api/icreat'
    # 업로드
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

    def test_delete(self):
        sub_num = self.req['sub_num']

        self.assertEqual(self.client.delete(f"{self.API}/{self.user_id}").status_code,
                        204)

        # 두번 삭제는 안됨
        self.assertEqual(self.client.delete(f"{self.API}/{self.user_id}").status_code,
                        400)


    def test_delete_failed(self):
        self.assertEqual(self.client.delete(f"{self.API}/12341234").status_code,
                        404)
