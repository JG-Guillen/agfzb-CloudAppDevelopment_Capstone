def get_dealer_reviews_from_cf(url, dealer_Id,**kwargs):
    results = []
    json_result = get_request(url,dealer_Id=dealer_Id)
    
    if json_result:
        for review_doc in json_result['Docs']:
            review_obj = CarDealer(address=review_doc["address"], city=review_doc["city"], full_name=review_doc["full_name"],
                                   id=review_doc["id"], lat=review_doc["lat"], long=review_doc["long"],
                                   short_name=review_doc["short_name"],
                                   st=review_doc["st"], zip=review_doc["zip"])
            results.append(review_obj)
    return results