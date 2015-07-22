import json
from django.http import HttpResponse
import requests
from decider_backend.settings import GOOGLE_API_KEY

SEND_ADDRESS = 'https://gcm-http.googleapis.com/gcm/send'

def send_push(reg_id, data, dry_run=False):

    session = requests.Session()
    request = requests.Request()
    request.method = 'POST'
    request.headers['Authorization'] = 'key=' + GOOGLE_API_KEY
    request.headers['Content-Type'] = 'application/json'
    request.url = SEND_ADDRESS

    request_data = {
        'to': reg_id,
        # 'registration_ids': [reg_id],
        'data': data
    }
    if dry_run:
        request_data.update({'dry_run': True})

    request.data = json.dumps(request_data)
    resp = session.send(request.prepare())
    response = HttpResponse(status=resp.status_code, content=resp.content)
    for h in resp.headers:
        setattr(response, h, resp.headers[h])

    return response
