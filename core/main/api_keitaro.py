import requests
import json

headers = {"Api-Key": ""}
server = ""


def get_clicks_and_conversations(range_to_body):
    url_clicks = server + "admin_api/v1/conversions/log"
    url_conversations = server + "admin_api/v1/clicks/log"
    """
    range = {
            "from": "2010-09-10",
            "to": "2022-09-10",
            "timezone": "UTC",
            "interval": None
        }
    """
    body = {
        "range": range_to_body,
        "limit": 1,
        "offset": 100,
        "columns": [],

        "filters": [
            {
                "name": "sub_id_6",
                "operator": "EQUALS",
                "expression": "bogdan"
            },
        ],

        "sort": [
            {
                "name": "clicks",
                "order": "ASC"
            }
        ]
    }
    response_clicks = requests.post(url=url_clicks, headers=headers, data=json.dumps(body))
    if response_clicks.status_code != 200:
        return False
    response_conversations = requests.post(url=url_conversations, headers=headers, data=json.dumps(body))
    if response_conversations.status_code != 200:
        return False

    return json.loads(response_clicks.text),  json.loads(response_conversations.text)
