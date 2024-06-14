from fastapi import FastAPI
from routers import inference
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
origins = [
    "https://sherlockvoice.ddnsking.com",
    "https://sherlock-voice.netlify.app",
    "http://3.37.244.252",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cookie 설정
    allow_methods=["*"],
    allow_headers=["*"],
)

# inference 라우터 추가
app.include_router(inference.router)
