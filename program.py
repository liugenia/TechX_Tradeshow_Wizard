import smartsheet

#https://smartsheet-platform.github.io/api-docs  SMARTSHEET API

smart = smartsheet.Smartsheet()  # uses 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID=5484659632039812
MAP_SHEET_ID=8844668382275460

# makes a new requests sheet, add to Tradeshow Map trigger=RYG trinary system
def create_sheet(name):
    sheet_spec = smartsheet.models.Sheet({
        'name': name,
        'columns': [
            {
            'title': 'Add to map?',
            'type': 'PICKLIST', #search 'column type' to see which type to use
            'symbol': 'RYG' # red = not added, yellow = add, green = already added
            }, {
            'title': 'Show Name',
            'type': 'TEXT_NUMBER',
            'primary': True,
            }, {
            'title': 'Setup Start Date',
            'type': 'DATE'
            }, {
            'title': 'Show Live Date',
            'type': 'DATE'
            }, {
            'title': 'Tear Down Date',
            'type': 'DATE'
            }, {
            'title': 'Program Manager',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Venue Name',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Location',
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

#handles the addition of a request row to the actual tradeshow map

def addRequest(sheet):
#1) call toAdd() to check if column in the sheet is "Yellow"
#2) if toAdd()==True, then copy that row to Tradeshow Map SS
#3) switch the value of 'Add to map' to "Green"
#4) call sortEntry() to place row in the right FY and Q, sorty by 'Show Live Date'
    pass

def toAdd(row, to_add='Yellow'):
    #checks the 'Add to map' column status (RYG), if "Yellow" the row needs to be added
    return row.cells[0].value==to_add

def switchAdd(row):
    #updates the 'Add to map' column value to "Green" to indicate row has been added to TSMap
    pass

def sortEntry(row):
#puts row into right place for Tradeshow Map SS
#1) calculate FY and Q of 'Show Live Date'
#2) if no header for FY and/or Q, append a title row
#3) for range of rows in given FY and Q -- sort by the Show Live date (index=3)
    pass

if __name__ == '__main__':
    # my_sheet = create_sheet('[TEST] ETS Service Request Form') --creates a new sheet, DONE