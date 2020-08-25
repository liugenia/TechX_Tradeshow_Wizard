from flask import Flask, request, Response

from program import MAP_SHEET_ID, process_sheet, REQUEST_SHEET_ID

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def respond():
    response = Response(status=200)
    print('Received POST request, here is the JSON:\n', request.json)

    if 'Smartsheet-Hook-Challenge' in request.headers:
        print('***Verification Request***')
        response.headers['Smartsheet-Hook-Challenge'] = request.headers['Smartsheet-Hook-Challenge']
        return response
    else:
        print('Running program.py')  # todo: add multithreading so we don't wait for program.py to finish
        process_sheet(REQUEST_SHEET_ID, MAP_SHEET_ID)
    return response
