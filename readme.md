![휴먼스케이프](https://user-images.githubusercontent.com/88444944/167796009-9b41d165-46e9-4bcc-b82e-7513e81ad8c8.jpg)


# Wanted team_B #3휴먼스케이프 기업과제  

임상정보 open API를 수집하는 WEB Aplication을 설계, 구현, 개발합니다.

## 과제 기한:
* 3 ~ 5인이 2 ~ 3일 이내로 완료하세요  
#
  1일: API분석, 모델링, 수집 스크립트(batch task) 작성

  2일: 임상정보 API 구현, 로컬 테스트 완료, API 문서화 

  3일: 배포 및 문서화, 가산점 구현(기능추가)

## Team process:

### Team 분업  ###  
  
|성명|업무|비고|
|------|---|---|
|최승리|배치스크립트 작성|팀장⭐ |
|하정현|배포(docker,swagger)|.|
|남기윤|데이터 적재 앱구현|.|\

### 중점 point

1. RESTFUL 한 API 구현 (Endpoint URL, HTTP Method , JSON Response)
2. 효율적인 쿼리 구현
3. 요구사항 뿐 아니라 다른 기능이 함게 있는 서버라고 가정하고 폴더, 파일, 코드 스트럭처를 설계

## Directory Info.

```
#최종 tree를 입력해주세요
```
## 실행 안내

_**Note**:_ django-contrab 실행에 필요한 fcntl이 Unix 계열 에만 존재합니다. 따라서 해당 Application은 **MacOS, Ubuntu 같은 Unix 기반 운영체제에서만 작동합니다.**
> **fcntl?** 
>
>  유닉스 체제에서는 일반 파일 뿐만 아니라 네트워크 소켓, 장치 등을 파일로 취급하고 관리합니다. fcntl은 이러한 유닉스 환경 속에서 파일들을 컨트롤 하기위해 제공되는 툴 입니다. 하지만 모든 리소스들을 파일로 취급하지 않는 Windows에서는 fcntl을 지원하지 않습니다.

### For Developers
해당 코드를 개작 또는 분석 하려는 개발자들을 대상으로 작성된 안내서 입니다.
1. repository를 다운받습니다.
    ```bash
    git clone https://github.com/2nd-wanted-pre-onboarding-team-b/HumanScape_Wanted.git
    ```
2. repository의 최상단에 .env 파일을 추가하고 파일 내용을 아래와 같이 작성합니다.
    ```bash
    SECRET_KEY=<DJango Secret Key>
    MYSQL_LOCAL_PASSWORD=<MySQL Password>
    ICREAT_URL="https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887"
    ICREAT_API_KEY=<INCREAT_URL에 대한 Api Key>
    URL="http://apis.data.go.kr/1352159/crisinfodataview/list"
    API_KEY=<url에 대한 api key>
    ```
3. MySQL을 작동시킵니다.
4. MySQL에 마이그레이션을 합니다.
    ```bash
    python manage.py migrate --settings=config.settings.local
    python manage.py makemigrations --settings=config.settings.local
    python manage.py migrate --settings=config.settings.local
    ```
5. 아래와 같이 명령어를 입력하여 Batch Process와 Application을 실행합니다.
    ```bash
    python manage.py contrab add --settings=config.settings.local
    python manage.py runserver --settings=config.settings.local
    ```
6. 단, 외부에서 접속을 원한다면 runserver 명령어에서 맨 마지막에 0.0.0.0:PORT를 추가합니다.
    ```
    python manage.py contrab add --settings=config.settings.local 0.0.0.0:[PORT]
    ```
7. 테스트 코드를 실행하고 싶은 경우, 아래와 같이 명렁어를 입력합니다.
    ```
    python manage.py test tests --settings=config.settings.local 0.0.0.0:[PORT]
    ```

### For Deployers
해당 어플리케이션을 배포하려는 배포자들을 대상으로 작성된 안내서 입니다.

1. repository를 다운받습니다.
    ```bash
    git clone https://github.com/2nd-wanted-pre-onboarding-team-b/HumanScape_Wanted.git
    ```
2. repository의 최상단에 .env 파일을 추가하고 파일 내용을 아래와 같이 작성합니다.
    * _**Note**_: MySQL Root 계정이 아닌 일반 계정에서는 작동하지 않습니다. User Password에서도 Root Password를 입력하십시오.
    ```bash
    SECRET_KEY=<DJango Secret Key>
    MYSQL_USER=root
    MYSQL_USER_PASSWORD=<ROOT Password>
    MYSQL_ROOT_PASSWORD=<ROOT Password>
    MYSQL_DATABASE=humanscape
    ICREAT_URL="https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887"
    ICREAT_API_KEY=<INCREAT_URL에 대한 Api Key>
    URL="http://apis.data.go.kr/1352159/crisinfodataview/list"
    API_KEY=<url에 대한 api key>
    ```
3. MySQL을 작동시킵니다.
4. Docker Network를 구성합니다. 모든 Docker Container들은 humanscape라는 이름의 network위에 작동하므로 humanscape 이름의 네트워크를 추가합니다.
    ```
    sudo docker network create humanscape
    ```
5. Docker Compose를 실행하면 서버가 작동됩니다.
    ```
    sudo docker compose up -d
    ```
6. 업데이트를 위해 서버를 재업로드를 할 경우 remove.sh를 이용해 container를 자운 다음 다시 생성합니다. 이때 MySQL Container는 지워지지 않습니다.
    ```
    sudo sh remove.sh
    sudo docker compose up -d
    ```

### TroubleShooting
#### For Developers
#### For Deployers
* MySQL은 작동이 되는데, Backend가 작동(대부분 마이그레이션)이 안되는 경우
  * MySQL Container와 DJango Container가 하나의 Network위에 있는 지 확인하십시오 아래와 같은 명령어를 입력하면 두 개의 컨테이너가 출력되어야 합니다.
      ```
      $ sudo docker network inspect humanscape
      [
        {
          "Name": "humanscape",
            ....생략...
        
        },
        {
          "Name": "humanscape_db",
            ....생략...
        }
      ]
      
      ```
      * 둘 중에 하나 이상이 없는 경우 해당 컨테이너와 네트워크를 전부 삭제하고 다시 네트워크를 생성하십시오.
      * 두개 다 연결되어 있는데도 작동이 안된다면, humanscape_db의 Docker IP(IPv4Address)를 확인합니다.
        ```
        $ sudo docker network inspect humanscape

        ... 생략 ...
        {
          "Name": "humanscape_db",
          ... 생략 ...
            "IPv4Address": "172.18.x.x"
        }
        ```
      * 그리고 docker-compose.yml의 MYSQL_HOST를 해당 Docker IP로 수정한 뒤, 다시 ```sudo docker compose up -d``` 를 수행합니다.
          ```yml
          docker-compose.yml

          services:
            humanscape_backend:
            ... 생략 ...
            environment:
              ...
              MYSQL_HOST: <Docker IP>
          ```
      *  **그래도 작동이 안된다면** 포트 연결, 방화벽 또는 포트 충돌 여부를 확인하십시오.

## 휴먼스케이프 project 요구사항 분석

* 임상시험 정보를 수집하는 batch task 작성
  * open API 참고:"htps://www.data.go.kr/data/3074271/fileData.do#/API목록/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887"
* 출제의도 :
  * open API 스펙을 보고 이해하며 데이터를 주기적으로 적재 하는 기능을 구현, 실제 데이터를 추가하면서 중복 방지에 대한 전략을 세워야함
  * 기존 데이터와 API 데이터간의 수정된 사항을 비교하여 해당 임상시험이 업데이트 된 것인지 새로 추가된 것 인지 구별이 가능해야함
  * 실행이 완료되면 추가된 건 수, 업데이트 된 건 수를 출력하거나 따로 로깅해줘야함
```
요구사항 분석
1. open API데이터를 적재하는 기능을 구현하며 중복을 방지하는 방법
  -여기에 내용을 입력해주세요
  
2.기존 데이터와 수정된 사항을 비교하여 구분하는 방법
  -여기에 내용을 입력해주세요
  
3.실행후 로깅 방법
  -여기에 내용을 입력해주세요
  
```
* 수집한 임상정보에 대한 API
  * 특정 임상정보 읽기(uuid 값은 자유)
* 수집한 임상정보 리스트 API
  * 최근 일주일 내에 업데이트 된 임상정보 리스트
  * pagination 기능
    * offset, limit로 구현
* 직접 API를 호출해서 볼 수 있는 API Document 작성
## 추가 도전과제(v2)

  * 임상시험 정보를 제공하는 다른 API를 스스로 발굴하여 batch task를 추가(가산점)
  * 배포하여 웹에서 사용 할 수 있도록 제공
    * README.md에 배포과정에 대한 가이등화 주소 제공, 설치하지 않고 확인가능한 경우 가산점
  * 임상정보 리스트 API
    * 검색기능 제공
    * pagination 기능: offset, limit구현후 새로운 방식을 제공하면 가산점

## API info.
  **request, response 둘 다 적어야합니다.
## DB info.

## 구현 과정

### 최승리
#### 임상시험 정보를 수집하는 batch task 작성
CRONTAB
1. django-crontab 사용 이유.
  * 상대적으로 구현이 간단하였고, 요구사항을 충분히 구현 가능 할 것으로 생각되었습니다.
2. 구현 방법.
  * `utils.py`에 open api로부터 데이터를 받아 올 수 있는 로직을 작성.
  * `icreat_batch.views.py`에 open api로부터 받은 데이터를 DB에 적재하고, 로깅하는 로직 작성.
3. 설정 방법 및 실행 방법.
  * `config.settings.base.py` 안에 `CRONJOBS` 부분을 수정하여 Schedule을 조정 할 수 있다.
  (현재 설정은 매주 월요일 오전 1시 실행)

  |분(0~59)|시(0~23)|일(0~31)|월(1~12)|요일(0~7)|
  |---|---|---|---|---|
  |*|*|*|*|*|

  * 요일에서 0과 1은 일요일이다.
  * 예 : (* 1 1 * *) = 매월 1일 오전 1시 실행
  * 스케줄링 설정 후 `python manage.py crontab add --settings=config.settings.local` 명령어를 사용하여 실행한다.
  * 삭제  `python manage.py crontab remove --settings=config.settings.local`
  * 조회  `python manage.py crontab show --settings=config.settings.local`
  * 실행 결과 데이터는 DB `icreat`테이블에 적재된다.
  * 에러로그는 프로젝트 root 경로내 `cron.log` 파일에 작성된다.(자동생성)
  * 실행로그는 DB `batch_log` 테이블에 적재된다.
4. 어려웠던 점.
* django_crontab도 결국 linux crontab을 작성해 주는 역할을 하는 것이지만, linux crontab을 직접 작성 하는 것보다 조금 까다로웠습니다. 저의 개발 환경은 WSL 환경이었고, 그로 인한 경로 에러와 버전 에러, 그리고 이유를 알 수 없는 무응답 에러 등이 있었습니다. 때문에 Ubuntu 22.04버전으로 듀얼부팅하여 재작성하였고 정상 작동하였습니다.

API
1. views를 사용하여 로직을 작성한 이유.
* 꼭 스케줄링을 통한 데이터 수집이 아닌, 수동으로 수집을 실행하는 경우도 있을 것으로 생각되었고, API로 간단히 실행한다면 사용성에서 더 나을것으로 생각 되었습니다.

2. 설명.
* open api로부터 전달 받은 데이터를 `Icreat.objects.create`로 데이터 생성합니다. `get_or_create`를 사용하지 않은 이유는. 만약 `unique`값인 과제 번호가 기존것과 중복된 것이 있다면 기존 데이터와 비교후 데이터가 적재되어야 하는데, `object` 형태로는 데이터 비교가 어려웠고, `queryset` 형태로 비교가 수월했기 때문입니다. 또한 추후 업데이트에서도 `queryset` 형태가 유리했습니다. 그래서 굳이 `get`을 할 필요성이 없다고 생각 되었습니다.
* 과제 번호가 중복된 것이 없다면 생성되고, 있다면 `IntegrityError` 예외처리를 통해 완전히 같은 데이터라면 `continue`, 하나의 값이라도 업데이트 된 것이 있다면, 전체 데이터를 덮어씁니다.
* 마지막으로 시작시간, 종료시간, 생성된 수, 업데이트된 수, 생성된 데이터의 과제번호 리스트, 업데이트된 데이터의 과제번호 리스트를 수집하여 `batch_log` 테이블에 로깅합니다.

3. 실행 방법.
* `METHOD = POST`, `api/v1/batch` 로 request합니다. `{'message' : "success!"}`가 출력되면 성공!
---
### 하정현
#### 배포 진행


![](https://raw.githubusercontent.com/Vector-7/Vector-7/master/1.PNG)


1. AWS EC2/RDS, GCP를 사용하지 않고 개인 서버를 사용한 이유
  * 1년전 과금을 문 이후(RDS를 한달 간 방치)로 일절 사용하지 않음
  * 프리티어가 만료되었으므로 1시간만 사용해도 비용이 발생
  * GCP도 마찬가지로 1년 무료 쿠폰(300$)이 만료됨
  * 리눅스 복기하는 의미로 개인서버에서 직접 배포 진행

2. 배포 전략
  * NginX
    * 최종 목표는 Swagger를 브라우저에 띄우는 것입니다. 단순히 Backend API만 배포한다면 포트가 외부로 열려있는 이상 프레임워크가 자체적으로 돌아가기 때문에 그냥 Backend를 열어놓고 CORS만 허용한다면 외부에서 접근이 가능하지만, 파일 형태로 존재하는 정적파일은 말 그대로 파일 상태로만 있기 때문에 이를 툴 없이 외부에서 접근한다는 것은 해킹 말고는 다른 방법이 없습니다. 그렇기 때문에 특정 url을 입력하면 바로 정적 파일로 이동시키는 Proxy Server를 새로 구축했습니다.
    * 아래의 코드는 /static에 접근하면  staticfiles의 정적 파일을 불러오는 역할을 하는 데, Swagger에서는 css/js 파일을 불러올 때 /static을 사용합니다. 따라서 static이 url에 포함되면, css/js파일이 있는 staticfiles로 이동하게 합니다.
      ```
      default
      # /statiuc
      location /static/ {
                alias /home/user/projects/HumanScape_Wanted/staticfiles/;
      }
      ```
  * Swagger 정적 파일 추출
    * 하지만 문제는 Swagger의 정적 파일이 어디있냐는 것입니다. 정적 파일을 추출하기 위해 ```python manage.py collectstatic``` 명령어로 정적파일을 추출할 수 있었습니다.

3. 보안 전략
  * 공유기에서 필요한 포트만 열어놓기
    * 서버에서 모든 포트를 열어놓으면 해킹의 위험이 높기 때문에 필요한 포트만 열어놓습니다.
  * Database 접근 제한
    * Backend까지는 Frontend에서 API요청을 해야 하므로 노출되도 무관하지만 Backend 뒤의 Resource들 (데이터베이스, 캐시 시스템, 일부 Private API Server...)은 밖으로 절때 노출되지 말아야 하고, 내부에서만 서로 통신하게 해야 합니다.
    * 해당 프로젝트에서는 데이터베이스가 3306번 포트로 동작하게 되는 데, 외부에 접근하지 못하게 공유기 상에서 포트를 막았습니다.
    * 그렇다면 데이터베이스는 내부 서버에서만 통신해야 하는 데, 다행이 데이터베이스와 백엔드는 Docker Container로 이루어져 있고 Docker Network를 통해 밖으로 노출되지 않은 채 서로 통신을 할 수 있었습니다.
  * SSH 접근 제한
    * 서버상에서 작업을 하려면 SSH를 필수 입니다. Password입력을 통한 Login은 Password가 해킹될 가능성이 있으므로 Password Login은 막아두고 오직 SSH Key로만 Login을 할 수 있게 설정했습니다.
      ```bash
      # /etc/ssh/sshd_config
      PasswordAuthentication no
      ```

4. 미처 못했던 부분들
  * Https 세팅
  * Github Action을 이용한 자동 배포
    * 과거에 CircleCI, TravisCI를 써봤기 때문에, Github Action의 Script작성도 기존 CI툴과 고만고만하다고 생각했지만, Github Action에서의 환경은 달랐습니다. 좀 더 Github Action에 대한 공부가 필요한 것 같습니다.

### 남기윤 (아래는 기본 양식입니다.)
  * 구현 기능 설명(캡쳐 이미지등을 활용해주세요)
  * 구현 방법과 이유 (이론적 설명을 포함해주시면 좋습니다. + ex)사용한 기술을 선정한 이유, 효율성, 확장성에대한 설명 등)
  * 구현과정에서 어려웠던 점 (100~200자 이내로 자유롭게 작성해주세요. 필수사항은 아닙니다.)
  * 구현 기능 설명2(필요 시 추가)
  * 구현 방법과 이유2
  * 구현 과정에서 어려웠던 점2
  * ...



