import requests
import urllib.parse
import datetime
#def generate(invoice_ids):
def generate():
    url = "https://script.google.com/macros/s/AKfycbxQosiG0A2fusp38-kt225jzvOff2T1sSqZ25IjYxGmMlsxOBVR/exec?"

    #invoice_ids = ["2"]
    invoice_ids = [{"name_of_user":"leke", "savings_product":"100001","posting_frequency":"monthly","date":datetime.date.today(),"amounted_credited":"20,000",
    "old_balance":"1000","available_balance":"30000"}]
    for invoice_id in invoice_ids:
        print("processing")
        payload = {"name_of_user":invoice_id['name_of_user'], "savings_product":invoice_id['savings_product'],"posting_frequency":invoice_id['posting_frequency'],"date":datetime.date.today(),"amounted_credited":invoice_id['amounted_credited'],
    "old_balance":invoice_id['old_balance'],"available_balance":invoice_id['available_balance']}
        u = url + urllib.parse.urlencode(payload)
        response = requests.get(u)
        print("file generated")
        response = requests.get(response.content)
        print(response.content)
        print("file downloaded")
        with open("invoice{}.pdf".format(invoice_id), "wb") as f:
            f.write(response.content)