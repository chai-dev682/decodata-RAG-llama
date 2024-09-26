import uvicorn
from fastapi import FastAPI, Request, Form
from config import load_env, ModelType
from src.agent import Agent

from typing import List
from src.models import Message

load_env()

app = FastAPI()

agent = Agent()


@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to the decodata LLM service!"}


@app.post("/prompt")
def process_prompt(messages: List[Message]):
    response = agent.invoke(messages=messages, model_type=ModelType.gpt4o)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
