"""Data models for PromptGuard Environment."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# Base classes - try openenv-core first, fallback to our own
try:
    from openenv.core.env_server import Action, Observation, State
except ImportError:
    class Action(BaseModel):
        """Base action model."""
        model_config = {"extra": "forbid"}
        metadata: Dict[str, Any] = Field(default_factory=dict)

    class Observation(BaseModel):
        """Base observation model."""
        model_config = {"extra": "forbid"}
        done: bool = False
        reward: Optional[Union[bool, int, float]] = None
        metadata: Dict[str, Any] = Field(default_factory=dict)

    class State(BaseModel):
        """Base state model."""
        model_config = {"extra": "allow"}
        episode_id: Optional[str] = None
        step_count: int = 0


class PromptGuardAction(Action):
    """Agent's defense configuration."""
    system_prompt: str = Field(..., description="The full defense system prompt text")
    defense_rules: List[str] = Field(..., description="Explicit defense rules")
    refusal_policy: str = Field(..., description="How to handle suspicious requests")
    allowed_topics: List[str] = Field(..., description="Topics the bot should engage with")
    blocked_patterns: List[str] = Field(..., description="Patterns/phrases that trigger refusal")


class PromptGuardObservation(Observation):
    """Observation returned after reset or step."""
    task_description: str = Field(default="", description="What persona to defend")
    persona_context: str = Field(default="", description="Background info and behavioral rules")
    example_legitimate_queries: List[str] = Field(default_factory=list)
    attack_categories: List[str] = Field(default_factory=list)
    current_step: int = Field(default=0)
    max_steps: int = Field(default=4)
    previous_score: Optional[float] = Field(default=None)
    defense_rate: Optional[float] = Field(default=None)
    utility_rate: Optional[float] = Field(default=None)
    feedback: Optional[str] = Field(default=None)


class PromptGuardState(State):
    """Episode state."""
    task_id: str = Field(default="easy")
    current_step: int = Field(default=0)
    max_steps: int = Field(default=4)
    best_score: float = Field(default=0.0)
    scores_history: List[float] = Field(default_factory=list)
    episode_complete: bool = Field(default=False)
