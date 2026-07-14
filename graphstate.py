from typing import Dict, List, Optional, TypedDict


class GraphState(TypedDict):
  
    question: Optional[str]


    interaction_text: Optional[str]
    voice_transcript: Optional[str]

    hcp_name: Optional[str]
    interaction_type: Optional[str]
    interaction_date: Optional[str]
    interaction_time: Optional[str]

    attendees: Optional[List[str]]

    topics_discussed: Optional[str]

 
    materials_shared: Optional[List[str]]
    samples_distributed: Optional[List[str]]

    sentiment: Optional[str]

 
    outcomes: Optional[str]
    follow_up_actions: Optional[str]

    ai_followups: Optional[List[str]]


    classification: Optional[str]

    extracted_entities: Optional[Dict]

    missing_fields: Optional[List[str]]

    validation_errors: Optional[List[str]]

    confidence_score: Optional[float]

    response: Optional[str]

    should_schedule_followup: Optional[bool]

    should_create_task: Optional[bool]

    should_add_sample: Optional[bool]

    should_add_material: Optional[bool]

    automation_result: Optional[Dict]

 
    log_status: Optional[str]

    error: Optional[str]