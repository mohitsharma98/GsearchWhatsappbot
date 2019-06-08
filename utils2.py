import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "customsearch.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "custom-search-ludvry"

from apiclient.discovery import build
api_key="AIzaSyARJ3eYy7G-Jxc_aDjU8QfecAScmFeVdXc"
resource = build('customsearch', 'v1', developerKey=api_key).cse()

def get_text(parameters):
    print(dict(parameters))
    p=0
    s=""
    print("-------------------------")
    for i in parameters['search_type']:
        s += "{} ".format(parameters['search_type'][p])
        p=p+1
    print(s)
    print("-------------------------")
    response = resource.list(q=s, cx="001380558770229582407:s9fgjefe8qi", num=5).execute()
    print(response)
    return response

def get_image(parameters):
    print(parameters)
    response = resource.list(q=parameters, cx="001380558770229582407:s9fgjefe8qi",searchType='image', num=1).execute()
    print(response['items'][0])
    return response

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    print(response)
    if response.intent.display_name == 'get_text':
        text = get_text(dict(response.parameters))
        print(text['items'][0])
        text_str = "Here is your search: "
        for row in text['items']:
            text_str += "\n\n{}\n\n{}\n\n".format(row['title'], row['link'])
        return str(text_str)
    elif response.intent.display_name == 'get_image':
        text = get_text(dict(response.parameters))
        print(text['items'][0])
        text_str = "Here is your image search: "
        for row in text['items']:
            text_str += "\n\n{}\n\n{}\n\n".format(row['title'], row['link'])
        return str(text_str)
    else:
        return response.fulfillment_text

# def fetch_reply(msg, session_id):
#     response = get_text(msg)
#     print(response)
#     text = get_text(msg)
#     print(text)
#     text_str = "Here is your search data: "
#     for row in text['items']:
#         text_str += "\n\n{}\n\n{}\n\n".format(row['title'], row['link'])
#     return text_str