from google.cloud import dialogflow_v2beta1 as dialogflow


def get_dialog_response(session_id, text, project_id):
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text,
        language_code=language_code
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    dialogflow_response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    response = {
        'query_text': dialogflow_response.query_result.query_text,
        'intent': dialogflow_response.query_result.intent.display_name,
        'confidence': dialogflow_response.query_result.intent_detection_confidence,
        'response_text': dialogflow_response.query_result.fulfillment_text,
    }
    
    return response
