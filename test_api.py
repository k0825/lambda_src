import requests
import pprint

url = 'https://3tu3wo8xsl.execute-api.us-east-2.amazonaws.com/dev/'
headers = {'Content-Type': 'application/json'}
data = {
    "operation_type": "SCAN"
}
req = requests.post(url=url, headers=headers, json=data)

pprint.pprint(req.text)
