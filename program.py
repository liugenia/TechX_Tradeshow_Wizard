import smartsheet
# from FY_Q_sort import calc_fy_q_hardcoded

smart = smartsheet.Smartsheet()  # uses 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID=4026093033285508
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
            'title': 'ETS Service Request?',
            'type': 'CHECKBOX',
            },{
            'title': 'Event Name',
            'type': 'TEXT_NUMBER',
            'primary': True,
            }, {
            'title': 'Move In Date',
            'type': 'DATE'
            }, {
            'title': 'Event Start Date',
            'type': 'DATE'
            }, {
            'title': 'Event End Date',
            'type': 'DATE'
            }, {
            'title': 'Cisco Program Manager (PM)',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Event Location (City, State/Country)',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Event Venue',
            'type': 'TEXT_NUMBER'
            }, {
            'title': "Booth Size (X' x Y')",
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
#1) call toAdd() to check if cell value of 'Add to map' is "Yellow"
#2) if toAdd(), copy that row to Tradeshow Map SS
#3) call markAdded() to switch the value of 'Add to map' to "Green"
#4) call delCols() to delete any extra columns imported
#5) call sortEntry() to place row in the right FY and Q, criteria: Event Start Date (Show Live)
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
            markAdded(sheet.id, row)
        delCols()
        # sortEntry(MAP_SHEET_ID)

#checks if the 'Add to map' column value is "Yellow" 
def toAdd(row):
    return row.cells[0].value=='Yellow'

#updates the 'Add to map' column value to "Green" to indicate row has been added
def markAdded(sheet_id, row):
    new_row = smartsheet.models.Row()
    new_row.id, new_row.cells = row.id, row.cells
    new_row.cells[0].value='Green'
    smart.Sheets.update_rows(sheet_id,[new_row])

#deletes the extra columns that aren't relevant
def delCols():
    sheet=smart.Sheets.get_sheet(MAP_SHEET_ID)
    for col in sheet.columns:
        if col.index>=13:
            smart.Sheets.delete_column(sheet.id, col.id)

#sorts the Tradeshow Map SS and puts entry in correct FY and Q
def sortEntry(sheet):
#1) calculate FY and Q of 'Show Live Date'
#2) check for FY/Q header row - if no header for FY and/or Q, append a row above
#3a) find the row value the FY/Q
#3b) sort the entry within the row range of given FY/Q
    pass

if __name__ == '__main__':
    # my_sheet = create_sheet('[TEST] ETS Service Request Form')
    transferRequest()