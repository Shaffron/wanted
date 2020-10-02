# Wanted Coding Test

## Enviroment
| product        | version  |
|----------------|----------|
| Python         | 3.8      |
| Docker Server  | 19.03.13 |
| Docker Client  | 19.03.13 |
| Docker Compose | 1.27.4   |
| SQLite3        | 3.20.9   |

## Set Up
```bash
cd {git cloned directory}
docker-compose up
```

## Requests
* .http 파일 실행을 지원하는 Jetbrains, VSCode 등의 IDE 가 있으면 디렉토리 내에 첨부된 <code>request.http</code> 파일로 API 를 테스트 할 수 있습니다.
* 아래 curl command 로도 실행 할 수 있습니다. (특수문자 escape 처리가 필요 할 수 있습니다.)
```bash
# 전체 회사 조회
curl -X GET localhost:5000/api/companies

# 이름으로 조회
curl -X GET localhost:5000/api/companies?keyword={name}&category=name

# 태그로 조회
curl -X GET localhost:5000/api/companies?keyword={tag}&category=tag

# 태그 삽입
curl -X POST -H "Content-Type: application/json" localhost:5000/api/companies/{company_id}/tag -d '{"tag":"태그_99"}'

# 태그 삭제
curl -X DELETE -H "Content-Type: application/json" localhost:5000/api/companies/{company_id}/tag -d '{"tag":"태그_99"}'
```

## Test
```
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt

python -m unittest --verbose tests/test_api.py
```