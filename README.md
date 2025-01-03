<div align="center">
 
# Sherlock Voice - BE 👩‍💻    

</div>

<br/> 

## ✅ 소개
**Sherlock Voice**는 AI를 활용해 보이스 피싱을 탐지하는 시스템입니다 <br/>
이 레포지토리는 프로젝트의 **백엔드 서버** 부분을 다루며, AI 모델 서빙과 API 제공을 담당합니다 <br/>
백엔드 서버는 AI 모델과 프론트엔드를 연결하고, 음성 데이터를 처리하여 사용자 신고 프로세스를 지원합니다 <br/>

<br/> 

## ✅ Sherlock Voice 주요 기능
- **AI 모델 서빙**: 보이스 피싱 탐지를 위한 AI 모델 호출 및 결과 반환
- **API 제공**: 프론트엔드와의 데이터 통신을 위한 RESTful API 구현
- **음성 데이터 처리**: 음성 파일을 텍스트로 변환하는 외부 API 연동
- **합성 음성 판별 모델**: SciPy-Cosine 유사도를 활용하여 입력된 오디오 백터와 가장 유사한 샘플의 라벨(fake,real)을 찾은 후 딥보이스 판별
- **보이스피싱 판별 및 위험도 측정 모델**: KoBERT 딥러닝 모델을 활용하여 데이터의 보이스피싱 여부와 위험도 측정
- **텍스트의 키워드 분석 및 보이스피싱 분류**: TextRank를 활용한 머신러닝 모델로 통화 내용의 키워드를 분석하여 제공하고 보이스피싱 유형에 맞는 대처법 제공

<br/> 

## ✅ 기술 스택
- **BE**: <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white">
- **AI 모델**: <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white"> <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=SciPy&logoColor=white"> <img src="https://img.shields.io/badge/KoBERT-FF7102?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/TextRank-8D5A9E?style=for-the-badge&logoColor=white">
- **외부 API**: <img src="https://img.shields.io/badge/Google Cloud-4285F4?style=for-the-badge&logo=Google Cloud&logoColor=white"> (Google Speech to Text API)

<br/> 

## ✅ Backend 설계
![BackendDesign](https://github.com/user-attachments/assets/f76ab4d4-b463-42be-a1e8-93d8c2ebe3cc)

<br/> 

## ✅ BE 폴더 구조
``` C
📦SherlockVoice_Server
 ┣ 📂models
 ┃ ┣ 📂kobert
 ┃ ┃ ┣ 📜BERTClassifier.py
 ┃ ┃ ┣ 📜BERTDataset.py
 ┃ ┃ ┣ 📜BERTSentenceTransform.py
 ┃ ┃ ┣ 📜KoBERT_model.py
 ┃ ┃ ┣ 📜get_kobert_model.py
 ┃ ┃ ┣ 📜kobert_tokenizer.py
 ┃ ┃ ┣ 📜requirements.txt
 ┃ ┃ ┣ 📜run.py
 ┃ ┃ ┗ 📜train_7epch.pt
 ┃ ┣ 📜deepfake_model.py
 ┃ ┣ 📜shuffle_400.csv
 ┃ ┗ 📜textrank_model.py
 ┣ 📂routers
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜inference.py
 ┣ 📂serverkey
 ┃ ┣ 📜sv-server.json
 ┃ ┗ 📜sv_key.pem
 ┣ 📜Dockerfile
 ┣ 📜main.py
 ┗ 📜requirements.txt
```

