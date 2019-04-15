import requests
import chat
import json


class Tuling(object):
    def __init__(self):
        pass

    @staticmethod
    def get_response(msg, image=None, user=None):
        apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
        config = chat.tuling_config
        perception = {
            "inputText": {
                "text": msg
            }
        }
        if image is not None:
            perception['inputImage'] = {
                "url": image
            }
        data = {
            "reqType": 0,
            "perception": perception,
            "userInfo": {
                "apiKey": config['key'],
                "userId": user if user is not None else 'wxChat'
            }
        }
        try:
            body = json.dumps(data)
            # print(json.dumps(data, ensure_ascii=False, indent=2))
            headers = {'Content-Type': 'application/json'}
            r = requests.post(apiUrl, data=body, headers=headers).json()
            # print(json.dumps(r, indent=2, ensure_ascii=False))
            return r.get('results')[0].get('values').get('text')
        except object:
            return


if __name__ == '__main__':
    response = Tuling.get_response("你好啊")
    print(response)
