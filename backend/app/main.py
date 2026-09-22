from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI(title="Profile Web API")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = MongoClient(MONGO_URL)
db = client["profile_db"]
profiles = db["profiles"]


@app.get("/")
def root():
    return {"message": "Profile Web API is running"}


@app.get("/api/profile")
def get_profile():
    profile = profiles.find_one({}, {"_id": 0})

    if not profile:
        profile = {
            "name": "請填入姓名",
            "school": "國立臺東大學",
            "department": "資訊工程學系",
            "bio": "這是我的個人簡介"
        }

    return profile
