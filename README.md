# 🌎 IS THIS NARA? 

### 프로젝트 개요

<img src="https://drive.google.com/uc?id=1nKRz1SGSUsXINUIkXHMrF_LBsTEPsbjg" alt="Logo Image" width="300" style="display: block; align:center;" />

#### 1. 프로젝트명
  - 주간 세계 뉴스 요약 자동화 뉴스레터 < IS THIS NARA? >
  
  
#### 2. 목적<br/>
  - 네이버 뉴스 중 ‘세계’ 카테고리의 뉴스들을 크롤링
  - 1주 간격으로 나누어 전처리, 요약, 분류하여 가장 많은 기사가 나온 TOP3 나라를 선정
  - TOP3 나라별 키워드 추출, 기사 요약 후 이를 뉴스레터로 제작하여 발송
  - 전체 프로세스 자동화하여 매주 발송될 수 있도록 설정


---
### 개발 프로세스


#### 1. 개발환경

<img alt="Python" src ="https://img.shields.io/badge/Python-3776AB.svg?&style=for-the-badge&logo=Python&logoColor=white"/> <img alt="HTML" src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white"/>

<img alt="EC2" src="https://img.shields.io/badge/Amazon EC2-FF9900.svg?style=for-the-badge&logo=Amazon EC2&logoColor=white"/>


#### 2. 프로세스(아키텍쳐)
  - 뉴스 기사 크롤링
    - BeautifulSoup
  - 텍스트 전처리 - 토큰화, 품사 태깅, 불용어 처리
      - konlpy, nltk
  - 요약 - 키워드 추출, 문서 요약, 문서 분류
      - summa
  - 뉴스레터 제작
      - html
  - 자동화 파이프라인 구축 - 신규 뉴스 기사 확인 후 DB에 적재, 데이터 전처리. 요약 후 메일 발송 프로세스 구축
      - AWS EC2

