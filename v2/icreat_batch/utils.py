import requests
import json, os
from urllib import parse


def get_data():
    """
        작성자 : 최승리
        공공 데이터 포털에서 open api 데이터 조회
    """
    url = os.environ.get('URL')
    api_key = os.environ.get('API_KEY')
    api_key_decode = parse.unquote(api_key)
    # open api가 요구하는 params
    params = {
        'page' : 1,
        'perPage' : 999,
        'returnType' : 'JSON',
        'serviceKey' : api_key_decode,
    }

    response = requests.get(url, params=params) # open api로 request
    json_data = json.loads(response.text) # 받은 데이터를 json 형식 변환
    return json_data # 최종 값 리턴
