import requests
from datetime import datetime

from django.db.utils import IntegrityError
from ..icreat.models import IcreatV2
from .utils import get_data ,set_batch_log, date_to_none

def batch_get_data():
    # 로깅을 위한 변수 SET
    created_count = 0
    updated_count = 0
    created_list = [] # 생성된 sub_num list
    updated_list = [] # 업데이트된 sub_num list

    start_time = datetime.now()

    batch_data = get_data() # open api로부터 데이터 조회(.utils.py)
    for data in batch_data:
        data = date_to_none(data)
        try:
            create_data = IcreatV2.objects.create(**data)
            created_list.append(create_data.trial_id)
            create_data.save()
            created_count += 1

        except IntegrityError: # trial_id값은 unique값이므로 중복 생성은 에러발생.
            exist_data = IcreatV2.objects.filter(trial_id=data["trial_id"]).values(*data.keys())
            if exist_data[0] == data:
                continue
            else:
                    # 기존에 데이터는 존재하지만 일부 수정이 생겼을 경우 UPDATE
                exist_data[0].update(**data, modified_at = datetime.now())
                updated_count += 1
                updated_list.append(exist_data[0]['trial_id'])
        except: #전처리 형식이 맞지 않는 데이터는 포기
            print(data)
    end_time = datetime.now()
    # 로그 테이블에 데이터 SET
    set_batch_log(start_time, end_time, created_count, updated_count, created_list, updated_list)
