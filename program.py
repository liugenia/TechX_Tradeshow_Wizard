import smartsheet
from FY_Q_sort import calc_fy_q_hardcoded

smart = smartsheet.Smartsheet()  # use 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID = 4026093033285508
MAP_SHEET_ID = 8844668382275460


# creates the smartsheet for ETS Tradeshow Map in the TechX workspace
def create_sheet(name):
    sheet_spec = smartsheet.models.Sheet({
        'name': name,
        'columns': [{
            'title': 'Show Name',
            'primary': True,
            'type': 'TEXT_NUMBER',
            }, {
            'title': 'Setup Start Date',
            'type': 'CHECKBOX',
            'symbol': 'STAR'
            }, {
            'title': 'Show Live Date',
            'type': 'TEXT_NUMBER'
            }, {
            'title': 'Tear Down Date',
            'type': 'TEXT_NUMBER'
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
            }]
        })
    response = smart.Home.create_sheet(sheet_spec)
    return response.result.id


def get_column_ids(sheet_id):
    columns = smart.Sheets.get_columns(
        sheet_id,
        include_all=True).data

    col_ids_names = [(column.id, column.name) for column in columns]
    return col_ids_names


def get_sheet(sheet_id):
    sheet = smart.Sheets.get_sheet(sheet_id)
    rows = sheet.rows
    for row in rows:
        if row.cells[0].value == 'Yellow':
            print(*(str(cell.value).ljust(22) for cell in row.cells[1:5]), sep=' ', end=' ')
            fy, q = calc_fy_q_hardcoded(row.cells[3].value)
            print(f'FY{fy} Q{q}')


# make a new requests sheet with added color dot column
# make a new map sheet for testing with original data, create fake data in requests and test adding it to the sheet
# pull in data from test requests sheet, print out new (yellow) rows with calculated FY/Q

# red = don't add, not added, yellow = add, green = don't add, already added

# implement fiscal year separations per Cisco calendar
# on run transfer of new row/information of a show,
# check if color circle is yellow
# find FY and Quarter row, create if doesn't exist
# add row to right spot within quarter
# change circle color to green


if __name__ == '__main__':
    # my_sheet = create_sheet('ETS Tradeshow Map Example')
    get_sheet(REQUEST_SHEET_ID)
