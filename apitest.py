import requests
import unicodedata
import json


def getHindiText(text):
    resultText = text
    try:
        url = 'https://hackapi.reverieinc.com/nmt'
        data_body = {'data': [text], 'src': 'en', 'tgt': 'hi'}
        headers = {'token': 'b9ad1696d2fb22f5536a932d3c8a7b5bfab4a644', 'Content-Type': 'application/json'}
        response = requests.post(url, json=data_body, headers=headers)
        x = response.content.decode("utf-8")
        decodedResult = json.loads(x)
        list_data = []
        list_data = decodedResult['data']['result']
        result_list = []

        for i in list_data:
            result_list.append(i[0])

        return result_list[0]
    except:
        print("erroraya")
        pass
    return resultText