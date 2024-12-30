# Sherlock Voice - Backend

## 소개
**Sherlock Voice**는 AI를 활용해 보이스 피싱을 탐지하는 시스템입니다.  
이 레포지토리는 프로젝트의 **백엔드 서버** 부분을 다루며, AI 모델 서빙과 API 제공을 담당합니다.  
백엔드 서버는 AI 모델과 프론트엔드를 연결하고, 음성 데이터를 처리하여 사용자 신고 프로세스를 지원합니다.

## Sherlock Voice 주요 기능
- **AI 모델 서빙**: 보이스 피싱 탐지를 위한 AI 모델 호출 및 결과 반환.
- **API 제공**: 프론트엔드와의 데이터 통신을 위한 RESTful API 구현.
- **음성 데이터 처리**: 음성 파일을 텍스트로 변환하는 외부 API 연동.
- **합성 음성 판별 모델**: SciPy-Cosine 유사도를 활용하여 입력된 오디오 백터와 가장 유사한 샘플의 라벨(fake,real)을 찾은 후 딥보이스 판별
- **보이스피싱 판별 및 위험도 측정 모델**: KoBERT 딥러닝 모델을 활용하여 데이터의 보이스피싱 여부와 위험도 측정
- **텍스트의 키워드 분석 및 보이스피싱 분류**: TextRank를 활용한 머신러닝 모델로 통화 내용의 키워드를 분석하여 제공하고 보이스피싱 유형에 맞는 대처법 제공

## 기술 스택
- **언어**: <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
- **프레임워크**: <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white">
- **AI 모델**: <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white"> <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=SciyPy&logoColor=white"> <img src="https://img.shields.io/badge/KoBERT-FF7102?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/TextRank-8D5A9E?style=for-the-badge&logoColor=white">
- **외부 API**: <img src="https://img.shields.io/badge/Google Speech-to-Text-4285F4?style=for-the-badge&logo=GoogleCloud&logoColor=white">

