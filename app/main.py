from fastapi import FastAPI
from app.api.deps import init_model

from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "https://8986-182-228-41-227.ngrok-free.app/",
    "https://955c-106-246-138-211.ngrok-free.app/mindmap"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    init_model()