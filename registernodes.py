workflow.add_node("classify_interaction", classify_interaction_node)

workflow.add_node("process_voice_note", process_voice_note_node)

workflow.add_node("extract_interaction_details", extract_interaction_details_node)

workflow.add_node("validate_interaction", validate_interaction_node)

workflow.add_node("generate_followups", generate_followups_node)

workflow.add_node("automation", automation_node)

workflow.add_node("log_interaction", log_interaction_node)

workflow.add_edge(
    "process_voice_note",
    "extract_interaction_details"
)

workflow.add_edge(
    "extract_interaction_details",
    "validate_interaction"
)

workflow.add_edge(
    "validate_interaction",
    "generate_followups"
)

workflow.add_edge(
    "generate_followups",
    "automation"
)

workflow.add_edge(
    "automation",
    "log_interaction"
)