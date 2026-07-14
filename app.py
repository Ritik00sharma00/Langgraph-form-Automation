import os
from typing import Any

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

from nodes import (
    automation_node,
    classify_interaction_node,
    extract_interaction_details_node,
    generate_followups_node,
    log_interaction_node,
    process_voice_note_node,
    validate_interaction_node,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "gemma2-9b-it"

app = FastAPI(title="MedicalAibot Backend")


def get_db_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set")

        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except Exception as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc


def get_groq_client() -> Any:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    try:
        from groq import Groq
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError(f"Groq SDK is not installed: {exc}") from exc

    return Groq(api_key=GROQ_API_KEY)


def run_medical_workflow(message: str, groq_response: str) -> dict[str, Any]:
    state: dict[str, Any] = {
        "question": message,
        "interaction_text": message,
        "voice_transcript": message,
        "hcp_name": "Auto-filled from AI input",
        "interaction_type": "AI Chat",
        "interaction_date": "2026-07-15",
        "interaction_time": "00:00",
        "attendees": [],
        "topics_discussed": message,
        "materials_shared": [],
        "samples_distributed": [],
        "sentiment": "neutral",
        "outcomes": groq_response,
        "follow_up_actions": "Review with care team",
        "ai_followups": [],
        "classification": "ai_chat",
        "extracted_entities": {},
        "missing_fields": [],
        "validation_errors": [],
        "confidence_score": 0.85,
        "response": groq_response,
        "should_schedule_followup": False,
        "should_create_task": False,
        "should_add_sample": False,
        "should_add_material": False,
        "automation_result": {},
        "log_status": "In Progress",
        "error": None,
    }

    state.update(classify_interaction_node(state))
    state.update(process_voice_note_node(state))
    state.update(extract_interaction_details_node(state))
    state.update(validate_interaction_node(state))
    state.update(generate_followups_node(state))
    state.update(automation_node(state))
    state.update(log_interaction_node(state))
    state["response"] = groq_response
    state["log_status"] = "Completed"

    return state


@app.get("/")
def read_root():
    return {"message": "MedicalAibot backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    connection = None

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        return {"status": "connected", "result": result}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
    finally:
        if connection is not None:
            connection.close()


@app.post("/chat")
def chat_with_groq(payload: dict[str, Any]):
    try:
        message = payload.get("message", "")
        if not message:
            return {"status": "error", "message": "message is required"}

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": message},
            ],
        )
        content = completion.choices[0].message.content or ""
        workflow_state = run_medical_workflow(message, content)

        return {
            "model": GROQ_MODEL,
            "response": content,
            "workflow": {
                "classification": workflow_state.get("classification"),
                "log_status": workflow_state.get("log_status"),
                "ai_followups": workflow_state.get("ai_followups"),
                "should_schedule_followup": workflow_state.get("should_schedule_followup"),
            },
        }
    except Exception as exc:
        return {"status": "error", "message": str(exc)}