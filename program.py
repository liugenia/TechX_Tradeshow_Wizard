import smartsheet
# from FY_Q_sort import calc_fy_q_hardcoded

#https://smartsheet-platform.github.io/api-docs  SMARTSHEET API

smart = smartsheet.Smartsheet()  # uses 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID=535070600652676
MAP_SHEET_ID=8844668382275460

# makes a new requests sheet, add to Tradeshow Map trigger=RYG trinary system
def create_sheet(name):
    sheet_spec = smartsheet.models.Sheet({
        'name': name,
        'columns': [
            {
            'title': 'ETS Status',
            'type': 'PICKLIST', #search 'column type' to see which type to use
            'symbol': 'RYG' # red = not added, yellow = add, green = already added
            }, {
            'title': 'Show Name',
            'type': 'TEXT_NUMBER',
            'primary': True,
            }, {
            'title': 'Setup Start',
            'type': 'DATE'
            }, {
            'title': 'Show Live',
            'type': 'DATE'
            }, {
            'title': 'Teardown',
            'type': 'DATE'
            }, {
            'title': 'Program Manager',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Location',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Venue Name',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Booth Size',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Booth Number',
            'type': 'TEXT_NUMBER'
            }]
        })
    response = smart.Home.create_sheet(sheet_spec)
    return response.result.id

#given ETS Service Request sheet, adds the relevant info to Tradeshow Map on click
def transferRequest():
#1a) call toAdd() to check if cell value of 'Add to map' is "Yellow"
#1b) call colToCopy() to ensure only matching columns are copied
#2) if toAdd() and colToCopy(), then copy that row to Tradeshow Map SS
#3) call switchAdd() to switch the value of 'Add to map' to "Green"
#4) call sortEntry() to place row in the right FY and Q, sort by 'Show Live Date'
    sheet=smart.Sheets.get_sheet(REQUEST_SHEET_ID)
    for row in sheet.rows:
        if toAdd(row):
            smart.Sheets.copy_rows(
                REQUEST_SHEET_ID,
                smartsheet.models.CopyOrMoveRowDirective({
                    'row_ids': [row.id],
                    'to': smartsheet.models.CopyOrMoveRowDestination({
                        'sheet_id': MAP_SHEET_ID
                    })
                })
            )
            switchAdd(sheet.id, row)
        # sortEntry(MAP_SHEET_ID)

#checks the 'Add to map' column status (RYG), if "Yellow" the row needs to be added
def toAdd(row):
    return row.cells[0].value=='Yellow'

#updates the 'Add to map' column value to "Green" to indicate row has been added
def switchAdd(sheet_id, row):
    new_row = smartsheet.models.Row()
    new_row.id, new_row.cells = row.id, row.cells
    new_row.cells[0].value='Green'
    smart.Sheets.update_rows(sheet_id,[new_row])

#compares column names for Request and Map SS, data copied for cols existing in both sheets
def colToCopy(sheet):
    # req_cols=smart.Sheets.get_sheet(REQUEST_SHEET_ID).columns
    # map_cols=smart.Sheets.get_sheet(MAP_SHEET_ID).columns
    pass

def sortEntry(sheet):
#puts row into right place for Tradeshow Map SS
#1) calculate FY and Q of 'Show Live Date'
#2) if no header for FY and/or Q, append a title row
#3) for range of rows in given FY and Q -- sort by the Show Live date (index=3)
    pass

if __name__ == '__main__':
    # my_sheet = create_sheet('[TEST] ETS Service Request Form')
    transferRequest()