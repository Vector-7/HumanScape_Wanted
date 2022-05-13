import datetime

from django.db import connection

from rest_framework.test import APITestCase

from apps.icreat.serializers import IcreatSerializer


"""
tab탭 구별되어 있고 없는 데이터는 null로 표시
총 14개가 있으며 이중 8개는 일주일 이내 수정된 데이터고
나머지 6개는 일주일 보다 훨씬 이전에 수정된 데이터다
출처: 질병관리청_임상연구 과제정보
출처 url(현재 접속 불가): https://www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887
"""
RAW_EXAMPLES = """C130010	조직구증식증 임상연구 네트워크 구축 및 운영(HLH)	Pediatrics	서울아산병원	120	3년	관찰연구	코호트	국내다기관
C130011	대한민국 쇼그렌 증후군 코호트 구축	Rheumatology	가톨릭대 서울성모병원	500	6년	관찰연구	코호트	국내다기관
C100002	Lymphoma Study for Auto-PBSCT	Hematology	가톨릭대 서울성모병원	null	1년	관찰연구	코호트	단일기관
C110007	악성림프종의 임상양상과 항암 화학요법의 치료 성적 조사 및 예후 예측 지표 분석, retrospective study	Hematology	가톨릭대 서울성모병원	200	null	관찰연구	Case-only	단일기관
C140012	우울증 임상연구네트워크구축	Psychiatry	가톨릭대 여의도성모병원	300	11개월	관찰연구	코호트	국내다기관
C160041	우울증 임상연구센터	Psychiatry	가톨릭대 여의도성모병원	1183	1년	관찰연구	코호트	국내다기관
C140004	소화성궤양 임상연구네트워크 구축사업	Gastroenterology	가톨릭대 인천성모병원	2000	24개월	관찰연구	코호트	국내다기관
C110005	희귀난치성질환 호흡재활 중앙관리센터 운영	Rehabilitation Medicine	강남세브란스병원	null	11개월	관찰연구	Case-only	단일기관
C110004	지속성외래복막투석(CAPD) 및 자동복막투석(APD) 환자의 삶의 질(QOL)을 비교하기 위한, 전향적, 다기관, 관찰연구	Nephrology	경북대학교병원	300	12개월	중재연구	Phase 4	국내다기관
C140014	제2형 당뇨병 임상연구네트워크 구축사업	Endocrinology	경희대학교병원	700	120개월	관찰연구	코호트	국내다기관
C160013	한국 노인노쇠 코호트 구축 및 중재 연구 사업	Family Medicine	경희대학교병원	3000	5년	관찰연구	코호트	국내다기관
C160014	병원 기반 당뇨병 예방 프로그램의 효과 비교를 위한 전향적 대조군 임상 연구	Endocrinology	경희대학교병원	744	3년	중재연구	Phase 4	국내다기관
C110011	병원 기반 인플루엔자 임상 네트워크	Infectious disease	고려대구로병원	null	null	관찰연구	Case-only	국내다기관
C140001	병원 기반 인플루엔자 임상 네트워크(소아청소년)	Pediatrics	고려대구로병원	null	null	관찰연구	Case-only	국내다기관"""

class TestappsIcreatReadQuery(APITestCase):
    """
    작성자: 하정현
    """
    API = '/api/icreat'


    @classmethod
    def setUpTestData(cls):

        # data parsing
        examples = RAW_EXAMPLES.split('\n')
        for i in range(len(examples)):
            
            # tab으로 문자열을 9개의 데이터로 쪼갠다.
            example = examples[i].split('\t')

            KEY_MAPS = ("sub_num", "subject", "meddept", "institute",
                        "goal_research", "period", "remark", "trial", "boundary")
            # 데이터가 "null"이면 추가하지 않는다.
            req = {KEY_MAPS[j]:example[j] for j in range(len(example)) if example[j] != 'null'}
            # DB Upload
            s = IcreatSerializer(data=req)
            s.is_valid()
            s.save()
            # i가 8 이상 (8, 9, 10, 11, 12, 13)은 수정 시간을 일주일 전 이상으로 바꾼다
            if i >= 8:
                t = datetime.datetime.now()- datetime.timedelta(days=20)
                time_str = t.strftime('%Y-%m-%d %H:%M:%S.%f')
                with connection.cursor() as cursor:
                    # model단에서 수정이 불가하기 때문에
                    # 직접 쿼리문으로 수정한다.
                    cursor.execute(f"UPDATE icreat set modified_at = '{time_str}' \
                        where sub_num = '{req['sub_num']}'")


    def test_query(self):
        """
        입력된 데이터는 14개
        그 중 일주일 이내 수정된 데이터는 8개다
        그런데 페이지 하나의 크기가 10 이므로
        8개의 데이터가 출력되어야 한다.
        """
        res = self.client.get(self.API)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        """ 데이터 확인용
        for d in data:
            sn = d['sub_num']
            obj = Icreat.objects.get(sub_num=sn)
            print(sn, obj.modified_at)
        """
        self.assertEqual(len(data), 8)
