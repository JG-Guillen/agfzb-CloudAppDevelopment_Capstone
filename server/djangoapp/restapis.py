import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import http.client
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url,**kwargs):
    if 'api_key' in kwargs:
        try:
            """
            params = {
                'text': kwargs['text'],
                'version': '2021-08-01',
                'features': 'sentiment',
                'return_analyzed_text': True
            }
            """
            api_key = kwargs['api_key']
            params=kwargs['params']
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=params, auth=HTTPBasicAuth('apikey', api_key))                                
        except:
            # If any error occurs
            print("Network exception occurred")
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    elif 'dealer_Id' in kwargs:
        conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")
        payload = "{\"dealership\":"+str(kwargs["dealer_Id"])+"}"
        headers = {
            'content-type': "application/json",
            'accept': "application/json"
            }

        conn.request("GET", url, payload, headers)

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
        return json_data
    else:
        conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")
        headers = { 'accept': "application/json" }
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    #print("url getcf: " + url)
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["rows"]
        # For each dealer object
        #print(json_result)
        for dealer_doc in json_result['Docs']:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_Id,**kwargs):
    results = []
    json_result = get_request(url,dealer_Id=dealer_Id)
    if json_result:
        #print(json_result)
        for review_doc in json_result['Docs']:
            print(review_doc["review"])
            review_obj = DealerReview(id=review_doc["id"], name=review_doc["name"], dealership=review_doc["dealership"],
                                    review=review_doc["review"], purchase=review_doc["purchase"],
                                   purchase_date=review_doc["purchase_date"],
                                   car_make=review_doc["car_make"], car_model=review_doc["car_model"],car_year=review_doc["car_year"],
                                   sentiment=analyze_review_sentiments(review_doc["review"]))
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c8398e37-e7c5-4aec-bbfa-dc90f26df3f9"
    api_key= "r6K_qf6xZPbxcDgRr3OaIvVBjdJ8MMpE0GosmmGzIHhH"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text,language="en",features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)
    return(response["sentiment"]["document"]["label"])

