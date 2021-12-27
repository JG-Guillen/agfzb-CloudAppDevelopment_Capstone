from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import json

def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c8398e37-e7c5-4aec-bbfa-dc90f26df3f9"
    api_key= "r6K_qf6xZPbxcDgRr3OaIvVBjdJ8MMpE0GosmmGzIHhH"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)
    return(label)

print(analyze_review_sentiments("great dealership, it is the best"))