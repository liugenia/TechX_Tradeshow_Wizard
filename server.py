from flask import Flask, request, Response

from program import MAP_SHEET_ID, process_sheet, REQUEST_SHEET_ID

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    response = Response(status=200)
    print('Received POST request.')
    print('Headers:\n', request.headers)
    print('JSON:\n', request.json)

    if 'Smartsheet-Hook-Challenge' in request.headers:
        print('***Verification Request***')
        response.headers['Smartsheet-Hook-Challenge'] = request.headers['Smartsheet-Hook-Challenge']
    else:
        print('Running program.py')  # todo: add multithreading so we don't wait for program.py to finish
        process_sheet(REQUEST_SHEET_ID, MAP_SHEET_ID)
    return response


@app.route('/')
@app.route('/admin')
def admin():
    return '<h1>Admin Page (Work In Progress)</h1>'
