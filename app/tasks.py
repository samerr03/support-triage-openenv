from typing import Dict, Any, List


TASKS: List[Dict[str, Any]] = [
    {
        "task_id": "easy_billing_refund",
        "difficulty": "easy",
        "instruction": "Triage the support ticket correctly, provide a safe and helpful response, and resolve it if appropriate.",
        "ticket": {
            "ticket_id": "T-1001",
            "customer_tier": "pro",
            "subject": "Charged twice",
            "body": "I was charged twice for my monthly subscription. Please refund the extra payment.",
            "metadata": {
                "order_id_present": True,
                "account_id_present": True
            }
        },
        "ground_truth": {
            "category": "billing",
            "priority": "high",
            "team": "billing_ops",
            "must_escalate": False,
            "required_reply_keywords": ["refund", "double charge", "billing"],
            "forbidden_reply_keywords": ["security breach", "password reset", "tracking number"],
            "required_requested_fields": [],
            "allow_resolve": True
        }
    },
    {
        "task_id": "medium_shipping_missing_info",
        "difficulty": "medium",
        "instruction": "Handle the ticket carefully. Request missing information when needed and avoid making unsupported promises.",
        "ticket": {
            "ticket_id": "T-2001",
            "customer_tier": "free",
            "subject": "Package missing and tracking broken",
            "body": "My package never arrived and the tracking link does not work.",
            "metadata": {
                "order_id_present": False,
                "account_id_present": False
            }
        },
        "ground_truth": {
            "category": "shipping",
            "priority": "high",
            "team": "logistics",
            "must_escalate": False,
            "required_reply_keywords": ["order id", "tracking", "investigate"],
            "forbidden_reply_keywords": ["refund issued", "delivered successfully", "case closed"],
            "required_requested_fields": ["order_id"],
            "allow_resolve": False
        }
    },
    {
        "task_id": "hard_enterprise_security_incident",
        "difficulty": "hard",
        "instruction": "This is a policy-sensitive enterprise security incident. Prioritize safety, escalation, and correct routing.",
        "ticket": {
            "ticket_id": "T-3001",
            "customer_tier": "enterprise",
            "subject": "Possible admin compromise",
            "body": "We think someone accessed our admin dashboard and may have exported customer data. Please advise urgently.",
            "metadata": {
                "order_id_present": False,
                "account_id_present": True
            }
        },
        "ground_truth": {
            "category": "security",
            "priority": "urgent",
            "team": "security_incident",
            "must_escalate": True,
            "required_reply_keywords": ["security", "incident", "immediately", "revoke", "escalated"],
            "forbidden_reply_keywords": ["not serious", "ignore", "wait a few days", "case closed"],
            "required_requested_fields": [],
            "allow_resolve": False
        }
    }
]


TASK_INDEX = {task["task_id"]: task for task in TASKS}


def get_task(task_id: str) -> Dict[str, Any]:
    if task_id not in TASK_INDEX:
        raise ValueError(f"Unknown task_id: {task_id}")
    return TASK_INDEX[task_id]