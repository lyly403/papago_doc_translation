import os
import time
import requests
import uuid
import urllib
from requests_toolbelt import MultipartEncoder

# API 인증 정보
client_id = '클라이언트 ID'
client_secret = '클라이언트 SECRET'

# 폴더 경로
input_folder = './before_KR'
output_folder = './tr_doc_gov_result'

def translate_document(file_path):
    data = {
        'source': 'ko',
        'target': 'en',
        'file': (file_path, open(file_path, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }

    m = MultipartEncoder(data, boundary=uuid.uuid4())
    headers = {
        "Content-Type": m.content_type,
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }

    url = "https://naveropenapi.apigw.gov-ntruss.com/doc-trans/v1/translate"
    response = requests.post(url, headers=headers, data=m.to_string())

    if response.status_code == 200:
        response_json = response.json()
        request_id = response_json.get('data', {}).get('requestId')
        print(f"번역 요청 성공, requestId: {request_id}")
        return request_id
    else:
        print(f"번역 요청 실패: {file_path}, 상태 코드: {response.status_code}")
        print("응답 내용:", response.text)
        return None

def check_translation_status(request_id):
    url = f"https://naveropenapi.apigw.gov-ntruss.com/doc-trans/v1/status?requestId={request_id}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get('data', {}).get('status')
            progress = response_json.get('data', {}).get('progressPercent', 0)

            if status == 'COMPLETE':
                print("번역이 완료되었습니다!")
                return True
            elif status == 'PROGRESS':
                print(f"현재 상태: {status}, 진행률: {progress}%")
            elif status == 'FAILED':
                print("번역이 실패했습니다.")
                return False
        else:
            print(f"상태 확인 요청 실패, 상태 코드: {response.status_code}")
            return False

        time.sleep(10)  # 상태 확인 간격 (예: 10초 후에 다시 확인)

def download_document(request_id, output_filename, output_folder):
    # 다운로드 URL 생성
    url = f"https://naveropenapi.apigw.gov-ntruss.com/doc-trans/v1/download?requestId={request_id}"
    
    # 헤더 설정
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('X-NCP-APIGW-API-KEY-ID', client_id),
        ('X-NCP-APIGW-API-KEY', client_secret)
    ]
    urllib.request.install_opener(opener)
    
    # 출력 경로 설정
    output_path = os.path.join(output_folder, output_filename)
    
    # 파일 다운로드
    urllib.request.urlretrieve(url, output_path)
    print(f"{output_filename} 파일이 성공적으로 다운로드되었습니다.")

def download_document2(request_id, output_filename, output_folder):
    url = f"https://naveropenapi.apigw.gov-ntruss.com/doc-trans/v1/download??requestId={request_id}"
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('X-NCP-APIGW-API-KEY-ID', client_id),
        ('X-NCP-APIGW-API-KEY', client_secret)
    ]
    urllib.request.install_opener(opener)

    output_path = os.path.join(output_folder, output_filename)

    urllib.request.urlretrieve(url, output_path)
    print(f"{output_filename} 파일이 성공적으로 다운로드되었습니다.")

# 시작 시간 측정용
total_start = time.time()
# 폴더 안의 파일을 하나씩 처리
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if os.path.isfile(file_path):  # 파일일 경우만 처리
        print(f"{filename} 번역 시작 중...")

        # 번역 요청
        request_id = translate_document(file_path)
        if request_id:
            # 번역 완료 여부 확인
            if check_translation_status(request_id):
                # 번역이 완료되면 다운로드
                output_filename = f"tr-{filename}"
                download_document(request_id, output_filename, output_folder)
                time.sleep(30)
            else:
                print(f"{filename} 번역 작업이 실패하였습니다.")
        else:
            print(f"{filename} 번역 요청에 실패하였습니다.")
# 종료 시간 측정
total_end = time.time()
print(f"프로그램 총 실행 시간: {total_end - total_start:.5f} sec")