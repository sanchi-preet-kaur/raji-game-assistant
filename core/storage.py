import json
import os
from datetime import datetime

STORE_DIR = os.path.join("data", "store")
LOGS_FILE = os.path.join(STORE_DIR, "chat_logs.json")
TICKETS_FILE = os.path.join(STORE_DIR, "support_tickets.json")


def _ensure_store():
    os.makedirs(STORE_DIR, exist_ok=True)
    for path in (LOGS_FILE, TICKETS_FILE):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f)


def log_interaction(question: str, answer: str, score: float, response_time: float, language: str) -> str:
    _ensure_store()
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)

    entry_id = f"chat_{len(logs) + 1}_{int(datetime.now().timestamp())}"
    logs.append({
        "id": entry_id,
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "score": round(score, 4),
        "response_time": round(response_time, 4),
        "language": language,
        "feedback": None,
    })

    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    return entry_id


def record_feedback(entry_id: str, feedback: str):
    _ensure_store()
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)

    for item in logs:
        if item["id"] == entry_id:
            item["feedback"] = feedback
            break

    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_logs() -> list:
    _ensure_store()
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ticket(name: str, email: str, category: str, message: str):
    _ensure_store()
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    tickets.append({
        "id": f"TKT-{1001 + len(tickets)}",
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "category": category,
        "message": message,
        "status": "Open",
    })

    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)


def get_tickets() -> list:
    _ensure_store()
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)