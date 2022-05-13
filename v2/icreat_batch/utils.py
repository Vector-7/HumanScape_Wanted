import requests
import json, os
from urllib import parse
from .models import BatchLogV2


def get_data():
    """
        작성자 : 남기윤
        공공 데이터 포털 질병관리청_임상연구 DB 에서 open api 데이터 조회
    """
    url = os.environ.get('ICREATV2_URL')
    api_key = os.environ.get('ICREATV2_API_KEY')
    api_key_decode = parse.unquote(api_key)
    # open api가 요구하는 params
    page_count = 1
    res = []
    while True:
        params = {
            'numOfRows' : 50,
            'pageNo' : page_count,
            'resultType' : 'JSON',
            'serviceKey' : api_key_decode,
        }
        response = requests.get(url, params=params).text # open api로 request
        items = json.loads(response)['items'] # 받은 데이터를 json 형식 변환 및 실험 list 가져오기
        if len(items) == 0:
            break
        res += items
        page_count += 1

    return res #종합된 리스트 반환

def set_batch_log(start_time, end_time, created_count, updated_count, created_list, updated_list):
    # 로그 테이블에 값 추가
    BatchLogV2.objects.create(
        start_time = start_time,
        end_time = end_time,
        created_count = created_count,
        updated_count = updated_count,
        created_list = created_list,
        updated_list = updated_list,
        )

def date_to_none(data):
    try:
        if data['date_registration'] == '':
            data['date_registration'] = None
        if data['date_updated'] == '':
            data['date_updated'] = None
        if data['date_enrolment'] == '':
            data['date_enrolment'] = None
        if data['results_date_completed'] == '':
            data['results_date_completed'] = None
    except:
        pass
    return data