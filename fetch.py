import requests
from app import config

class Fetch:
    def get(url):
        bearerToken = 'Bearer ' + config['PERSONAL_ACCESS_TOKEN']
        header = {'Authorization': bearerToken}
        response = requests.get(url, headers=header)
        return response.json()
        
    def patch(url):
        bearerToken = 'Bearer ' + config['PERSONAL_ACCESS_TOKEN']
        header = {'Authorization': bearerToken}
        response = requests.patch(url, headers=header)
        return response.json()

    def post(url, files, data):
        bearerToken = 'Bearer ' + config['PERSONAL_ACCESS_TOKEN']
        header = {'Authorization': bearerToken}
        response = requests.post(url, files=files, data=data, headers=header)
        return response.json()
