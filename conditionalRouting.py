def decide_input_type(state: GraphState):
    """
    Decide whether input came from voice or manual form.
    """

    if state.get("voice_transcript"):
        return "extract_interaction_details"

    return "process_voice_note"



workflow.add_conditional_edges(
    "classify_interaction",
    decide_input_type,
    {
        "process_voice_note": "process_voice_note",
        "extract_interaction_details": "extract_interaction_details",
    },
)