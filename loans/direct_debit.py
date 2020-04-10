import requests
import json
def directDebit(auth_code, email, amount):
    url = "https://api.paystack.co/charge"
    headers = {
        'Authorization': 'Bearer sk_test_9ca1f494d9bf0659064e00bb62d664657df83577',
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'cookie': 'J8JBNpPEVEjx3QA4zTpn'
    }
    datum = {
        "email": email,
        "amount": amount,
        "authorization_code": auth_code
    }
    x = requests.post(url, data=json.dumps(datum), headers=headers)
    results = x.json()
    return results
#print(directDebit("AUTH_nbd2sdkqkb","lexmill99@gmail.com","500000"))
