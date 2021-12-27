import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import http.client


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url,**kwargs):
    if 'dealer_Id' in kwargs:
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
        print("hola2")
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
        print(json_result)
        for review_doc in json_result['Docs']:
            
            review_obj = DealerReview(id=review_doc["id"], name=review_doc["name"], dealership=review_doc["dealership"],
                                    review=review_doc["review"], purchase=review_doc["purchase"],
                                   purchase_date=review_doc["purchase_date"],
                                   car_make=review_doc["car_make"], car_model=review_doc["car_model"],car_year=review_doc["car_year"],
                                   sentiment="")
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



