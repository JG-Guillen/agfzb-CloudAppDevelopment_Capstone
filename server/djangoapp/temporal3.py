from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import json
from datetime import datetime
""""
def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c8398e37-e7c5-4aec-bbfa-dc90f26df3f9"
    api_key= "r6K_qf6xZPbxcDgRr3OaIvVBjdJ8MMpE0GosmmGzIHhH"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text,language="en",features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)
    return(response["sentiment"]["document"]["label"])

print(analyze_review_sentiments("Great service!"))
"""

import http.client

conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")

payload = "{\"id\":5332476239}"

headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
review={}
review["dealership"] = 11
review["review"] = "This is a great car dealerrrrr"
json_payload={}
json_payload["review"]=review
conn.request("POST", "/api/review/api/review", json.dumps(json_payload), headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
