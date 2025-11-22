from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from interact_with_persona import chat_loop
from run_persona_survey import run_persona_survey_json
import uvicorn
from typing import Optional
from predictor import predict_party
from pymongo import MongoClient
import os
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rishikesh:nzGnd3PK9rhT65OG@tccl-pre-prod-local.u7ngf.mongodb.net/voter-ai?retryWrites=true&w=majority&appName=tccl-pre-prod-local")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["voter_ai"]
collection = db["synthetic_profiles"]

class QueryRequest(BaseModel):
    constituency: str

class ChatRequest(BaseModel):
    profile: dict
    question: Optional[str] = None


@app.post("/api/chat")
def chat_with_persona(req: ChatRequest):
    try:
        result = chat_loop(req.profile, req.question)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/interview")
def interview_persona(req: ChatRequest):
    response = run_persona_survey_json(req.profile)
    return response

@app.post("/api/prediction")
def predict_party_api(req: dict):
    predicted_result = predict_party(req)
    return {"predicted_party": predicted_result}

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


@app.post("/persona/query")
async def persona_query(req: QueryRequest):
    profile = fetch_profiles_by_constituency(req.constituency)

    if not profile:
        raise HTTPException(status_code=404, detail="Constituency not found in MongoDB")

    return {"profile": profile}

def fetch_profiles_by_constituency(constituency: str):
    cursor = collection.find(
        {"synthetic_voter_profile.geographic_context.constituency": {"$regex": f"^{constituency}$", "$options": "i"}}
    )
    
    profiles = []
    for doc in cursor:
        doc.pop("_id", None)
        profiles.append(doc)

    return profiles

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
