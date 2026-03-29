"""FastAPI application for PromptGuard environment."""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from promptguard.models import PromptGuardAction, PromptGuardObservation, PromptGuardState
from promptguard.server.environment import PromptGuardEnvironment

app = FastAPI(
    title="PromptGuard",
    description="Prompt Injection Defense Environment for OpenEnv",
    version="0.1.0",
)

# Global environment instance
env = PromptGuardEnvironment()

# Dashboard data store
_dashboard_data: Dict[str, Any] = {}

STATIC_DIR = Path(__file__).parent / "static"


class ResetRequest(BaseModel):
    task_id: str = "easy"
    seed: Optional[int] = None
    episode_id: Optional[str] = None


class StepRequest(BaseModel):
    system_prompt: str
    defense_rules: List[str] = []
    refusal_policy: str = ""
    allowed_topics: List[str] = []
    blocked_patterns: List[str] = []


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/reset")
async def reset(request: ResetRequest):
    try:
        obs = env.reset(
            seed=request.seed,
            episode_id=request.episode_id,
            task_id=request.task_id,
        )
        return obs.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
async def step(request: StepRequest):
    try:
        action = PromptGuardAction(
            system_prompt=request.system_prompt,
            defense_rules=request.defense_rules,
            refusal_policy=request.refusal_policy,
            allowed_topics=request.allowed_topics,
            blocked_patterns=request.blocked_patterns,
        )
        obs = await env.step_async(action)

        # Update dashboard data
        _dashboard_data.update({
            "task_id": env.state.task_id,
            "current_step": env.state.current_step,
            "score": obs.reward,
            "defense_rate": obs.defense_rate,
            "utility_rate": obs.utility_rate,
            "scores_history": list(env.state.scores_history),
            "best_score": env.state.best_score,
            "feedback": obs.feedback,
            "done": obs.done,
        })

        return obs.model_dump()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
async def state():
    return env.state.model_dump()


@app.get("/dashboard")
async def dashboard():
    dashboard_path = STATIC_DIR / "dashboard.html"
    if not dashboard_path.exists():
        return JSONResponse(
            content={"message": "Dashboard not yet available"},
            status_code=404,
        )
    return FileResponse(dashboard_path)


@app.get("/dashboard/data")
async def dashboard_data():
    return _dashboard_data


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
