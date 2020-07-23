import smartsheet
from FY_Q_sort import calc_fy_q_hardcoded

smart = smartsheet.Smartsheet()  # use 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID = 4026093033285508
MAP_SHEET_ID = 8844668382275460


def process_sheet(sheet_id, simulate=False):  # main loop for processing the sheet
    rows_to_update = []
    sheet = smart.Sheets.get_sheet(sheet_id)
    rows = sheet.rows
    col_ids_names = get_columns_id_and_title(sheet_id)
    print_col_headings(col_ids_names)
    for i, row in enumerate(rows):
        if check_row(row):
            print_row(row)
            new_row = update_row_status(row, color='Green')
            if new_row:  # checks that the new row was updated successfully
                rows_to_update.append(new_row)
    if not simulate:
        smart.Sheets.update_rows(sheet_id, rows_to_update)
    else:
        print('\nSimulation! These rows would have been updated to green:')
        for row in rows_to_update:
            print(str(row.id).ljust(20), row.cells[1].value)


def get_columns_id_and_title(sheet_id):  # returns a list of (id, title) tuples of all columns in sheet
    columns = smart.Sheets.get_columns(
        sheet_id,
        include_all=True).data
    col_ids_names = [(column.id, column.title) for column in columns]
    return col_ids_names


def check_row(row, index=0, val_to_test='Yellow'):  # checks if the given cell in the given row is the given value
    return row.cells[index].value == val_to_test


def print_col_headings(cols):  # prints the column name and id for the 2 - 7th column
    print(*(str(col[1]).ljust(24) for col in cols[1:6]), 'Start FY/Quarter')
    print(*(str(col[0]).ljust(24) for col in cols[1:6]), end='\n\n')


def print_row(row):  # prints the 2 - 7th column in the passed-in row, + FY/Quarter with some fancy formatting
    print(*((str(cell.value)[:22] + (str(cell.value)[22:] and '..')).ljust(24) for cell in row.cells[1:6]),
          sep=' ', end=' ')
    fy, q = calc_fy_q_hardcoded(row.cells[3].value)
    print(f'FY{fy} Q{q}')


def update_row_status(row, color='Green'):
    # creates a new row object with the old row's id and cells, updates the first cell to the passed in color
    new_row = smartsheet.models.Row()
    new_row.id, new_row.cells = row.id, row.cells
    try:
        assert color in ['Red', 'Yellow', 'Green']
        new_row.cells[0].value = color
    except AssertionError:
        print(f"Color must be one of: 'Red', 'Yellow', 'Green'. Color was {color}")
        return None
    except Exception as e:
        print(e)
        return None
    return new_row

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
    process_sheet(REQUEST_SHEET_ID, simulate=True)
