from typing import Dict, Any
from app.graders import grade_state


def state_signature(state) -> tuple:
    return (
        state.current_category,
        state.current_priority,
        state.current_team,
        state.drafted_reply,
        tuple(state.requested_fields),
        state.escalated,
        state.resolved
    )


def shaped_reward(prev_state, new_state, task: Dict[str, Any]) -> Dict[str, Any]:
    prev_score = grade_state(prev_state, task)
    new_score = grade_state(new_state, task)

    delta = new_score - prev_score
    step_penalty = -0.01

    loop_penalty = 0.0
    if state_signature(prev_state) == state_signature(new_state):
        loop_penalty = -0.03

    reward = delta + step_penalty + loop_penalty

    return {
        "score": round(reward, 4),
        "components": {
            "progress_delta": round(delta, 4),
            "step_penalty": step_penalty,
            "loop_penalty": loop_penalty
        },
        "message": "Trajectory reward with progress shaping"
    }