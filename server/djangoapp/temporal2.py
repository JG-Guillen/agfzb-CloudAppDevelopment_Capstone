import requests
import json
from requests.auth import HTTPBasicAuth
import http.client
from ibm_watson import NaturalLanguageUnderstandingV1
from datetime import datetime

def post_request(url, json_payload, **kwargs):
    conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")
    headers = {
        'content-type': "application/json",
        'accept': "application/json"
        }
    payload=json_payload
    conn.request("POST", "/api/review/api/review", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

url = "/api/review/api/review"
review={}
#review["time"] = datetime.utcnow().isoformat()
review["dealership"] = 11
review["review"] = "This is a great car dealer"
json_payload={}
json_payload["review"]=review
#print(json.dumps(json_payload))
post_request(url, json.dumps(json_payload))