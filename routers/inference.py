from fastapi import APIRouter, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile
from hashlib import sha256
import io
import wave
import os
from google.cloud import speech
from multiprocessing import Process
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models.deepfake_model import run_audio_classifier
from models.textrank_model import summarize_keywords
from models.kobert.KoBERT_model import inference, inf

# Google STT API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/Final_Server/routers/sv-server.json"

router = APIRouter()

result = {}  # 결과를 저장할 딕셔너리

# 오디오 샘플 속도 가져오기
def get_sample_rate(content):
    with wave.open(io.BytesIO(content), "rb") as wave_file:
        return wave_file.getframerate()

# 오디오 샘플 채널 가져오기
def get_sample_channels(content):
    with wave.open(io.BytesIO(content), "rb") as wave_file:
        return wave_file.getnchannels()

# 오디오 변환 및 텍스트 추출
async def transcribe_audio(content, sample_rate_hertz, sample_channels, filename):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code="ko-KR",
        model="default",
        audio_channel_count=sample_channels,
        enable_automatic_punctuation=True,
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=90)

    transcriptions = {}
    if response.results:
        for res in response.results:
            transcriptions[filename] = res.alternatives[0].transcript

    else:
        print("Not able to transcribe the audio file")

    return transcriptions, summarize_keywords(transcriptions)

def kobert_model(text):
    
    test_eval, confidence = inference(text)

    kobert_output = {
        "test_eval": test_eval,
        "confidence": confidence
    }
    
    return kobert_output

@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()

    # 임시 파일 생성 및 내용 쓰기
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(content)
    temp_file.close()
    
    file_name = temp_file.name  # 임시 파일 이름 사용
    
    # 파일 이름 해싱 및 정수로 변환
    task_id = int(sha256(file.filename.encode()).hexdigest(), 16) % 1000000
    
    # Store the file path and content in result for processing in the waiting endpoint
    result[task_id] = {"file_name": file_name, "content": content}

    return {"task_id": task_id}

# 대기 엔드포인트
@router.get("/waiting/{task_id}")
async def waiting(task_id: int):
    # 작업 완료 여부 확인
    if task_id in result and "file_name" in result[task_id]:
        # Process the file if not yet processed
        file_name = result[task_id]["file_name"]
        content = result[task_id]["content"]
        
        deepfake_result = run_audio_classifier(file_name)
        
        if 'fake' in deepfake_result[file_name]['result']:
            result[task_id].update({"Deepfake_check": True})
        else:
            transctiptions, keywords = await transcribe_audio(content, get_sample_rate(content), get_sample_channels(content), file_name)
        
            kobert_output = kobert_model(transctiptions[file_name])
            
            if kobert_output["test_eval"] == "보이스피싱 전화":
                result[task_id].update({
                    "Deepfake_check": False,
                    "VoicePhishing": kobert_output["test_eval"],
                    "VoicePhishing_prob": round(kobert_output["confidence"]),
                    "Keywords": keywords
                })
            else: 
                result[task_id].update({
                    "Deepfake_check": False,
                    "VoicePhishing": kobert_output["test_eval"],
                    "VoicePhishing_prob": round(kobert_output["confidence"]),
                    "Keywords": keywords
                })

        # Clean up temporary data to save memory
        del result[task_id]["file_name"]
        del result[task_id]["content"]
        
        return {"status": "ready"}
    else:
        return {"status": "processing"}


# 결과 가져오기 엔드포인트
@router.get("/result/{task_id}")
async def get_result(task_id: int):
    if task_id in result:
        if len(result[task_id]) == 1:
            return {"Deepfake_check": result[task_id]["Deepfake_check"]}
        elif len(result[task_id]) == 2:
            return {"Deepfake_check": result[task_id]["Deepfake_check"], 
                    "VoicePhishing": result[task_id]["VoicePhishing"],
                    "VoicePhishing_prob": result[task_id]["VoicePhishing_prob"],
                    "Keywords": result[task_id]["Keywords"]}
        else:
            return {"Deepfake_check": result[task_id]["Deepfake_check"], 
                    "VoicePhishing": result[task_id]["VoicePhishing"],
                    "VoicePhishing_prob": result[task_id]["VoicePhishing_prob"],
                    "Keywords": result[task_id]["Keywords"]}
    else:
        return {"error": "No result available or closest_match_prob_percentage not calculated yet"}
