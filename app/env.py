from copy import deepcopy
from typing import Tuple, Optional

from app.models import Observation, Action, Reward, Info, EnvironmentState, Ticket
from app.tasks import TASKS, get_task
from app.reward import shaped_reward
from app.graders import grade_state


class SupportTriageEnv:
    def __init__(self, task_id: str = "easy_billing_refund", max_steps: int = 8):
        self.task_id = task_id
        self.max_steps = max_steps
        self._task = get_task(task_id)
        self._state: Optional[EnvironmentState] = None
        self.reset(task_id=task_id)

    def _build_observation(self) -> Observation:
        return Observation(
            task_id=self._state.task_id,
            difficulty=self._state.difficulty,
            instruction=self._state.instruction,
            step_index=self._state.step_index,
            max_steps=self._state.max_steps,
            ticket=self._state.ticket,
            current_category=self._state.current_category,
            current_priority=self._state.current_priority,
            current_team=self._state.current_team,
            drafted_reply=self._state.drafted_reply,
            requested_fields=self._state.requested_fields,
            escalated=self._state.escalated,
            resolved=self._state.resolved,
            action_history=self._state.action_history,
            available_actions=[
                "classify",
                "set_priority",
                "assign_team",
                "draft_reply",
                "request_info",
                "escalate",
                "resolve"
            ]
        )

    def reset(self, task_id: Optional[str] = None) -> Observation:
        if task_id is not None:
            self.task_id = task_id

        self._task = get_task(self.task_id)
        ticket_data = self._task["ticket"]

        self._state = EnvironmentState(
            task_id=self._task["task_id"],
            difficulty=self._task["difficulty"],
            instruction=self._task["instruction"],
            step_index=0,
            max_steps=self.max_steps,
            ticket=Ticket(**ticket_data),
            current_category=None,
            current_priority=None,
            current_team=None,
            drafted_reply=None,
            requested_fields=[],
            escalated=False,
            resolved=False,
            action_history=[],
            done=False,
            cumulative_reward=0.0
        )

        return self._build_observation()

    def state(self) -> EnvironmentState:
        return deepcopy(self._state)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        if self._state.done:
            obs = self._build_observation()
            reward = Reward(score=0.0, components={}, message="Episode already done")
            info = Info(
                grader_score=grade_state(self._state, self._task),
                task_complete=True,
                mistakes=["Episode already completed"],
                notes={"cumulative_reward": self._state.cumulative_reward}
            )
            return obs, reward, True, info.model_dump()

        prev_state = deepcopy(self._state)
        mistakes = []

        try:
            if action.action_type == "classify":
                self._state.current_category = action.payload.get("category")

            elif action.action_type == "set_priority":
                self._state.current_priority = action.payload.get("priority")

            elif action.action_type == "assign_team":
                self._state.current_team = action.payload.get("team")

            elif action.action_type == "draft_reply":
                self._state.drafted_reply = action.payload.get("reply", "")

            elif action.action_type == "request_info":
                field_name = action.payload.get("field")
                if field_name:
                    if field_name not in self._state.requested_fields:
                        self._state.requested_fields.append(field_name)
                    else:
                        mistakes.append(f"Field already requested: {field_name}")
                else:
                    mistakes.append("Missing field name in request_info")

            elif action.action_type == "escalate":
                if self._state.escalated:
                    mistakes.append("Already escalated")
                self._state.escalated = True

            elif action.action_type == "resolve":
                self._state.resolved = True

            else:
                mistakes.append(f"Unknown action_type: {action.action_type}")

        except Exception as e:
            mistakes.append(f"Action processing error: {str(e)}")

        self._state.action_history.append({
            "step": self._state.step_index + 1,
            "action_type": action.action_type,
            "payload": action.payload
        })

        self._state.step_index += 1

        if self._state.step_index >= self._state.max_steps or self._state.resolved:
            self._state.done = True

        reward_data = shaped_reward(prev_state, self._state, self._task)
        self._state.cumulative_reward += reward_data["score"]

        grader_score = grade_state(self._state, self._task)

        obs = self._build_observation()
        reward = Reward(**reward_data)
        info = Info(
            grader_score=grader_score,
            task_complete=self._state.done,
            mistakes=mistakes,
            notes={
                "cumulative_reward": round(self._state.cumulative_reward, 4),
                "difficulty": self._state.difficulty
            }
        )

        return obs, reward, self._state.done, info.model_dump()

    def list_tasks(self):
        return [
            {
                "task_id": t["task_id"],
                "difficulty": t["difficulty"],
                "instruction": t["instruction"]
            }
            for t in TASKS
        ]