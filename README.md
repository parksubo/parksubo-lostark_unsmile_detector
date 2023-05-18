# parksubo-lostark_unsmile_detector

# 아키텍쳐
![image](https://github.com/parksubo/parksubo-lostark_unsmile_detector/assets/33623096/35e34e29-f53e-4961-89ed-932003e645a2)

# 프로젝트 요약
- Smilegate의 오픈소스 AI 및 LostArk 자유게시판 데이터를 이용한 악성 게시글 검출
    - (a) - 로스트아크 자유게시판의 데이터를 크롤링하여 데이터셋 생성
        - 닉네임, 제목, 등록일의 데이터 포함한 데이터셋 추출
            - 컴퓨터 자원 문제로 인해 15000개의 데이터 셋이서 구간별로 뽑은 약 3300개의 데이터셋만을 활용
    - (b) - kafka producer에서 smilegate-ai(baseline) 모델을 사용하여 특정 채팅 유형 검사
        - Docker 환경에서 kafka와 zookeeper 사용에서 AWS EC2 환경으로 아키텍쳐 변경 [링크](https://subo0521.tistory.com/200)
        - score가 0.5 이상인 label을 해당 게시글의 유형으로 판단
            - label이 clean일 경우 CLEAN_DATA_TOPIC, label이 clean이 아닐 경우 UNSMILE_DATA_TOPIC으로 구분
        - 토픽별로 consumer를 설정
            - UNSMILE_DATA_TOPIC인 경우 elasticsearch로 데이터 전송
    - (c) - 파악된 채팅 유형을 elasticsearch에 적재 및 kibana로 시각화하여 유저별 악성 게시글 등록 횟수 및 유형 파악
        - 아래 차트로 구성
            - 유저별 악성 게시글 등록 횟수에 대한 막대차트
            - 날짜별 악성 게시글 갯수에 Area 라인차트
            - 악성 게시글 유형에 대한 막대차트
            - unsmile score 분포에 대한 라인차트