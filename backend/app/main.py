from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import secrets

app = FastAPI(title="Profile Web API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

COUCHDB_URL = os.getenv("COUCHDB_URL", "http://couchdb:5984")
COUCHDB_USER = os.getenv("COUCHDB_USER", "admin")
COUCHDB_PASSWORD = os.getenv("COUCHDB_PASSWORD")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

DB_NAME = "profile_db"
DOC_ID = "profile"

# 儲存目前有效的登入 token
active_tokens = set()


class LoginRequest(BaseModel):
    password: str


class ProfileUpdate(BaseModel):
    name: str
    school: str
    department: str
    bio: str


def auth():
    return (COUCHDB_USER, COUCHDB_PASSWORD)


def check_token(authorization: str | None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="尚未登入")

    token = authorization.replace("Bearer ", "", 1)

    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="登入已失效")


@app.get("/")
def root():
    return {"message": "Profile Web API is running"}


@app.post("/api/login")
def login(data: LoginRequest):
    if not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Server administrator password is not configured"
        )

    if not secrets.compare_digest(data.password, ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="密碼錯誤")

    token = secrets.token_urlsafe(32)
    active_tokens.add(token)

    return {"token": token}


@app.get("/api/profile")
def get_profile():
    db_response = requests.put(
        f"{COUCHDB_URL}/{DB_NAME}",
        auth=auth()
    )

    if db_response.status_code not in (201, 202, 412):
        raise HTTPException(
            status_code=500,
            detail="Unable to initialize database"
        )

    response = requests.get(
        f"{COUCHDB_URL}/{DB_NAME}/{DOC_ID}",
        auth=auth()
    )

    if response.status_code == 200:
        data = response.json()

        return {
            "name": data.get("name", ""),
            "school": data.get("school", ""),
            "department": data.get("department", ""),
            "bio": data.get("bio", "")
        }

    if response.status_code == 404:
        profile = {
            "_id": DOC_ID,
            "name": "陳宣穎",
            "school": "國立臺東大學",
            "department": "資訊工程學系",
            "bio": "我是資工三甲陳宣穎"
        }

        create_response = requests.put(
            f"{COUCHDB_URL}/{DB_NAME}/{DOC_ID}",
            json=profile,
            auth=auth()
        )

        if create_response.status_code not in (201, 202):
            raise HTTPException(
                status_code=500,
                detail="Unable to create profile"
            )

        profile.pop("_id")
        return profile

    raise HTTPException(
        status_code=500,
        detail="Unable to read profile"
    )


@app.put("/api/profile")
def update_profile(
    profile: ProfileUpdate,
    authorization: str | None = Header(default=None)
):
    check_token(authorization)

    response = requests.get(
        f"{COUCHDB_URL}/{DB_NAME}/{DOC_ID}",
        auth=auth()
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Unable to read current profile"
        )

    current = response.json()

    updated_profile = {
        "_id": DOC_ID,
        "_rev": current["_rev"],
        "name": profile.name,
        "school": profile.school,
        "department": profile.department,
        "bio": profile.bio
    }

    save_response = requests.put(
        f"{COUCHDB_URL}/{DB_NAME}/{DOC_ID}",
        json=updated_profile,
        auth=auth()
    )

    if save_response.status_code not in (201, 202):
        raise HTTPException(
            status_code=500,
            detail="Unable to save profile"
        )

    return {"message": "個人資料修改成功"}
