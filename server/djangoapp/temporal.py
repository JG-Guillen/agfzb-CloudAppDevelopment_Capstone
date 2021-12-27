import requests
import json
from requests.auth import HTTPBasicAuth
import http.client


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url,**kwargs):
    if 'dealer_Id' in kwargs:
        conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")
        payload = "{\"dealership\":"+str(kwargs["dealer_Id"])+"}"
        print("payload: " +payload)
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


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in json_data['Docs']:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealer_Id,**kwargs):
    results = []
    json_result = get_request(url,dealer_Id=dealer_Id)
    
    if json_result:
        for review in json_result['Docs']:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            print(review["review"])
            """
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
            """
    
    return json_result
    #return results
"""
import http.client

conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")

headers = { 'accept': "application/json" }

conn.request("GET", "/api/dealership/api/dealership", headers=headers)

res = conn.getresponse()
data = res.read()
#print(data.decode("utf-8"))
json_data = json.loads(data)

#print(data.decode("utf-8"))
for dealer in json_data['Docs']:
    # Get its content in `doc` object
    print(dealer["full_name"])
"""
"""
import http.client

conn = http.client.HTTPSConnection("a6e41465.us-south.apigw.appdomain.cloud")
payload = "{\"dealership\":15}"
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

conn.request("GET", "/api/review/api/review", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
"""
#url = "/api/dealership/api/dealership"
#dealerships = get_dealers_from_cf(url)
#print(dealerships)

url = "/api/review/api/review"
dealer_Id=15
reviews = get_dealer_reviews_from_cf(url, dealer_Id)
# Concat all dealer's short name
#print(reviews)