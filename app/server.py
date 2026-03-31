from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.env import SupportTriageEnv
from app.models import Action

app = FastAPI(title="Support Triage OpenEnv", version="0.1.0")

env = SupportTriageEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy_billing_refund"


@app.get("/")
def root():
    return {
        "status": "ok",
        "name": "support-triage-openenv",
        "message": "Customer Support Triage OpenEnv is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def tasks():
    return {"tasks": env.list_tasks()}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs}


@app.get("/state")
def state():
    return env.state().model_dump()


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }