import requests
import json
def ddebitCode(email, amount, no, cvv, month, year):
    url = "https://api.paystack.co/charge"
    headers = {
        'Authorization': 'Bearer sk_test_9ca1f494d9bf0659064e00bb62d664657df83577',
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'cookie': 'J8JBNpPEVEjx3QA4zTpn'
    }
    """datum = {
        "email": email,
        "amount": amount,
        "card": {
        "number":no,
        "cvv":cvv,
        "expiry_month":month,
        "expiry_year":year
        }"""
    datum = {
        "email": email,
        "amount": amount,
        "card": {
        "number":no,
        "cvv":cvv,
        "expiry_month":month,
        "expiry_year":year
        }
    }
    x = requests.post(url, data=json.dumps(datum), headers=headers)
    results = x.json()
    return results['data']['authorization']['authorization_code']


#print(ddebitCode("lexmill99@gmail.com", "10000", "4084084084084081", "408", "02", "22"))


