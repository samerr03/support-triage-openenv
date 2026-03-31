from typing import Dict, Any, List


def keyword_hits(text: str, keywords: List[str]) -> float:
    if not keywords:
        return 1.0
    text = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text)
    return hits / len(keywords)


def keyword_penalty(text: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    text = text.lower()
    bad = sum(1 for kw in keywords if kw.lower() in text)
    return bad / len(keywords)


def grade_state(state, task: Dict[str, Any]) -> float:
    gt = task["ground_truth"]

    category_score = 1.0 if state.current_category == gt["category"] else 0.0
    priority_score = 1.0 if state.current_priority == gt["priority"] else 0.0
    team_score = 1.0 if state.current_team == gt["team"] else 0.0

    if gt["required_requested_fields"]:
        req = set(gt["required_requested_fields"])
        got = set(state.requested_fields)
        info_score = len(req & got) / len(req)
    else:
        info_score = 1.0

    escalate_score = 1.0 if state.escalated == gt["must_escalate"] else 0.0

    reply_text = (state.drafted_reply or "").lower()
    required_reply_score = keyword_hits(reply_text, gt["required_reply_keywords"])
    forbidden_penalty = keyword_penalty(reply_text, gt["forbidden_reply_keywords"])
    reply_score = max(0.0, required_reply_score - 0.5 * forbidden_penalty)

    if gt["allow_resolve"]:
        resolved_score = 1.0 if state.resolved else 0.0
    else:
        resolved_score = 1.0 if not state.resolved else 0.0

    score = (
        0.20 * category_score +
        0.15 * priority_score +
        0.15 * team_score +
        0.10 * info_score +
        0.15 * escalate_score +
        0.20 * reply_score +
        0.05 * resolved_score
    )

    score = max(0.0, min(1.0, score))
    return round(score, 4)