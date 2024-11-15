# papago_doc_translation
papago_doc_translation API with Python

## 개요
- papago 문서 번역 자동화 POC를 위해 제작
- 공공기관용, 민간용 제작 
  

## 기술 스택
- Python3
- Naver Cloud platform
- papago Translation API 

## 참고 사항
- 이미지로 된 텍스트는 번역 불가
- 텍스트에 적용된 스타일은 일부 일치하지 않거나 누락될 수 있음
- 텍스트에 적용된 링크나 액션은 일부 동작하지 않거나 누락될 수 있음
- 암호가 설정된 파일 미지원
- 읽기 전용 파일 미지원
- 이미 번역 진행 단계에 있는 문서가 있을 경우, API 동시 호출 제한

### 지원 포멧
- .docx, .pptx, .xlsx, .pdf, .hwp

## 시나리오
이 API는 다음과 같은 사용자들을 위해 설계되었습니다:
- 네이버클라우드 플랫폼에서 제공하는 papago translation Test
- 여러개의 문서를 한 폴더에 모아 순차적으로 자동 번역&다운로드
- NCP 공공기관/민간 사용자
  
## 주요 기능
- API 키 부분을 사용자에 알맞게 수정
- 번역할 문서(Before) 폴더 지정
- 번역한 문서(After) 폴더 지정
- 클라우드 플랫폼 성격 별 요청 URL 상이 #수정 필요


