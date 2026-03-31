# Support Triage OpenEnv

A real-world OpenEnv environment that simulates customer support ticket triage.  
This environment is designed to evaluate AI agents on realistic support workflows such as classification, prioritization, routing, escalation, information gathering, and reply drafting.

---

## Motivation

Customer support triage is a real operational task used by SaaS companies, e-commerce teams, and enterprise support organizations.

This environment models a realistic workflow where an agent must:
- classify incoming support tickets
- assign the right priority
- route to the correct internal team
- ask for missing details when necessary
- escalate security incidents
- draft a safe and helpful response

This makes it useful for benchmarking AI agents in a practical domain instead of games or toy tasks.

---

## Environment API

The environment follows the OpenEnv-style structure with typed Pydantic models.

### Core methods

- `reset()` → returns initial observation
- `step(action)` → returns observation, reward, done, info
- `state()` → returns current full state

---

## Observation Space

Each observation contains:

- `task_id` : current task identifier
- `difficulty` : easy / medium / hard
- `instruction` : task objective
- `step_index` : current step number
- `max_steps` : max allowed steps
- `ticket` :
  - `ticket_id`
  - `customer_tier`
  - `subject`
  - `body`
  - `metadata`
- `current_category`
- `current_priority`
- `current_team`
- `drafted_reply`
- `requested_fields`
- `escalated`
- `resolved`
- `action_history`
- `available_actions`

---

## Action Space

Allowed actions:

### 1. classify
```json
{"action_type":"classify","payload":{"category":"billing"}}
{"action_type":"set_priority","payload":{"priority":"high"}}
{"action_type":"assign_team","payload":{"team":"billing_ops"}}
{"action_type":"draft_reply","payload":{"reply":"We are sorry for the double charge. Our billing team will review and assist with the refund."}}
{"action_type":"request_info","payload":{"field":"order_id"}}
{"action_type":"escalate","payload":{}}
{"action_type":"resolve","payload":{}}