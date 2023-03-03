import csv
import requests

url = 'http://x/x/v2/x/x'
proxy_url = 'http://localhost:8888'
filename = 'filename.csv'

proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def checkCardAlias(customerID, cardID, headers):
    print(f"CustomerID: {customerID} CardID: {cardID}") 

    #response = requests.get(url, headers=headers)
    response = requests.get(url, headers=headers, proxies=proxies)

    response.raise_for_status()
    data = response.json()

    last_four = None

    #last_four = data['response']['stored'][0]['card']['lastFour']
    for stored_payment in data['response']['stored']:
        if stored_payment['cardID'] == int(cardID):
            last_four = stored_payment['card']['lastFour']

    if last_four is None:
        print('Card alias is empty')
    else:
        print(f'Card alias {last_four}')

with open(filename, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        customerID = row['CustomerID']
        cardID = row['CardID']

        headers = {
        'accept': 'application/json',
        'customer-id': customerID,
        'correlation-id': 'x'
        }

        try:
            checkCardAlias(customerID, cardID, headers)
        except requests.exceptions.HTTPError as err:
            print('Request failed with error:', err)
        except Exception as ex:
            print('An unexpected error occurred:', ex)