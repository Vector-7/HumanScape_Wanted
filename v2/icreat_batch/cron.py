import requests


def batch_req():
    url = "http://localhost:8000/api/v1/batch"
    return requests.post(url)
