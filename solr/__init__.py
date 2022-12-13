# import requests
# from decouple import config

# solr_url = config('SOLR_URL')


# def store_to_solr(data):
#     response = requests.post(solr_url+'/update/json/docs?commit=true',
#                              headers={'Content-Type': 'application/json'},
#                              json=data)
#     print('response: ', response)
#     print('response.text: ', response.text)

#     return response.json()
