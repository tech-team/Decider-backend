import json
from django.http import HttpResponse
import requests
from decider_backend.settings import GOOGLE_API_KEY

SEND_ADDRESS = 'https://gcm-http.googleapis.com/gcm/send'

def send_push(reg_id, notification, data, dry_run=True):

    session = requests.Session()
    request = requests.Request()
    request.method = 'POST'
    request.headers['Authorization'] = 'key=' + GOOGLE_API_KEY
    request.headers['Content-Type'] = 'application/json'
    request.url = SEND_ADDRESS

    request_data = {
        'to': reg_id,
        'notification': notification,
        'data': data
    }
    if dry_run:
        request_data.update({'dry_run': True})

    request.data = json.dumps(request_data)
    response = session.send(request.prepare())
    return HttpResponse()
