import threading
from pprint import pprint

from flask import Flask, request, Response

from program import CHANGE_AGENT, MAP_SHEET_ID, process_sheet, REQUEST_SHEET_ID

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req_json = request.json

    response = Response(status=200)
    print('\n----------------------')
    print('Received POST request.')
    print('Headers:')
    print(request.headers)
    print('JSON:')
    pprint(req_json)
    print('\n')

    if req_json:
        if 'challenge' in req_json:
            print('***Verification Request***')
            return {'smartsheetHookResponse': req_json['challenge']}

        elif 'events' in req_json:
            if all(CHANGE_AGENT in event.get('changeAgent', '') for event in req_json['events']):
                print('Received callback due to updates that were all caused by this program; ignoring to avoid loops')
            else:
                print('***Running program.py***')
                threading.Thread(target=process_sheet, args=[REQUEST_SHEET_ID, MAP_SHEET_ID]).start()
        else:
            print('Invalid request, no action taken (JSON in body did not match any expected pattern)')
    else:
        print('Invalid request, no action taken (no JSON in body)')
    return response


@app.route('/')
@app.route('/admin')
def admin():
    return '<h1>Admin Page (Work In Progress)</h1>'
