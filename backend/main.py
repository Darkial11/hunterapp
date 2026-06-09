from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

from routes import user, missions, rewards

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HunterAPP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(missions.router)
app.include_router(rewards.router)

@app.get("/")
def root():
    return {"status": "HunterAPP API running"}