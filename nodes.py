from graphstate import GraphState


def classify_interaction_node(state: GraphState):
    """
    Classify the incoming request.
    Examples:
    - Manual Form Entry
    - Voice Note
    - AI Chat
    """
    return {
        "classification": "manual_entry"
    }


def process_voice_note_node(state: GraphState):
    """
    Convert voice recording into text.
    """
    return {
        "voice_transcript": state.get("interaction_text")
    }


def extract_interaction_details_node(state: GraphState):
    """
    Extract HCP information from transcript/text.
    """
    return {
        "hcp_name": state.get("hcp_name"),
        "interaction_type": state.get("interaction_type"),
        "interaction_date": state.get("interaction_date"),
        "interaction_time": state.get("interaction_time"),
        "attendees": state.get("attendees"),
        "topics_discussed": state.get("topics_discussed"),
        "materials_shared": state.get("materials_shared"),
        "samples_distributed": state.get("samples_distributed"),
        "sentiment": state.get("sentiment"),
        "outcomes": state.get("outcomes"),
        "follow_up_actions": state.get("follow_up_actions"),
    }


def validate_interaction_node(state: GraphState):
    """
    Validate mandatory fields.
    """
    missing = []

    if not state.get("hcp_name"):
        missing.append("hcp_name")

    if not state.get("interaction_type"):
        missing.append("interaction_type")

    if not state.get("interaction_date"):
        missing.append("interaction_date")

    return {
        "missing_fields": missing
    }


def generate_followups_node(state: GraphState):
    """
    Generate AI suggested follow-up actions.
    """
    return {
        "ai_followups": [
            "Schedule follow-up meeting",
            "Send product brochure",
            "Share clinical trial data"
        ]
    }


def automation_node(state: GraphState):
    """
    Decide automation actions.
    """
    return {
        "should_schedule_followup": True,
        "should_create_task": True,
        "log_status": "Ready for CRM Logging"
    }


def log_interaction_node(state: GraphState):
    """
    Final CRM Logging.
    """
    return {
        "response": "Interaction logged successfully.",
        "log_status": "Completed"
    }