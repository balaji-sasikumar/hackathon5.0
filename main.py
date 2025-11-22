from fastapi import FastAPI
from pydantic import BaseModel
from interact_with_persona import chat_loop
from run_persona_survey import run_persona_survey_json
import uvicorn

app = FastAPI()

class ChatRequest(BaseModel):
    profile: dict
    question: str


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

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
