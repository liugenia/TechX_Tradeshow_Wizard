import smartsheet

from FY_Q_sort import calc_fy_q_hardcoded

smart = smartsheet.Smartsheet()  # use 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID = 4026093033285508
MAP_SHEET_ID = 8844668382275460


def process_sheet(request_sheet_id, map_sheet_id, simulate=False):  # main loop for processing the sheet
    rows = smart.Sheets.get_sheet(request_sheet_id).rows
    column_mapping = column_name_to_id_map(request_sheet_id)

    print_col_headings(column_mapping)

    for row in rows:
        if check_row(row, column_mapping):
            print_row(row)
            if not simulate:
                send_row(sheet_id=map_sheet_id,
                         row=row,
                         request_column_mapping=column_mapping)
                smart.Sheets.update_rows(request_sheet_id,
                                         update_row_status(row=row,
                                                           color='Green'))
            else:
                print('Simulation! This row would have been updated to green and added to the map sheet.\n')


def send_row(sheet_id, row, request_column_mapping):
    fy, q = calc_fy_q_hardcoded(get_cell_by_column_name(row=row,
                                                        column_name='Event Start Date',
                                                        col_map=request_column_mapping).value)
    fy_q_dict = make_fy_q_dict(sheet_id)

    new_row = smartsheet.models.Row()
    new_row.parent_id = get_quarter_parent_id(fy, q, fy_q_dict)
    new_row.to_bottom = True

    map_column_mapping = column_name_to_id_map(sheet_id)

    for cell in row.cells:
        if reverse_dict_search(request_column_mapping, cell.column_id) in map_column_mapping.keys():
            new_cell = smartsheet.models.Cell()
            new_cell.value = cell.value
            new_cell.column_id = map_column_mapping[reverse_dict_search(request_column_mapping, cell.column_id)]
            new_row.cells.append(new_cell)

    smart.Sheets.add_rows(sheet_id, new_row)


def update_row_status(row, color='Green'):
    # creates a new row object with the old row's id and cells, updates the first cell to the passed in color
    allowed_colors = ['Red', 'Yellow', 'Green']
    new_row = smartsheet.models.Row()
    new_row.id, new_row.cells = row.id, row.cells
    try:
        assert color in allowed_colors
        new_row.cells[0].value = color
        return new_row
    except AssertionError:
        print(f"Color must be one of: {allowed_colors}. Color was {color}. Row will not be updated")
    return row


def check_row(row, column_mapping, column_name='ETS Status', val_to_test='Yellow'):
    return get_cell_by_column_name(row, column_name, column_mapping).value == val_to_test


def print_col_headings(cols):  # prints the column name and id for the 2 - 7th column
    print(*(column_format(col_title) for col_title in cols.keys()), 'Start FY/Quarter')
    print(*(str(col_id).ljust(23) for col_id in cols.values()), end='\n\n')


def print_row(row):  # prints the 2 - 7th column in the passed-in row, + FY/Quarter with some fancy formatting
    print(*(column_format(cell.display_value or cell.value) for cell in row.cells), sep=' ', end=' ')
    fy, q = calc_fy_q_hardcoded(row.cells[3].value)
    print(f'FY{fy} Q{q}')


def column_format(item, just=23):
    return (str(item)[:just - 2] + (str(item)[just - 2:] and '..')).ljust(just)


def column_name_to_id_map(sheet_id):  # returns a title:id dict of all columns in sheet
    return {column.title: column.id for column in smart.Sheets.get_columns(sheet_id, include_all=True).data}


def get_cell_by_column_name(row, column_name, col_map):
    return row.get_column(col_map[column_name])  # {NAME: ID}


def reverse_dict_search(search_dict, search_value):
    for key, val in search_dict.items():
        if val == search_value:
            return key


def make_fy_q_dict(sheet_id):
    fy_q_dict = {str(fy.cells[0].value): [fy, {}] for fy in find_fy_rows(sheet_id)}
    for year, (year_row, _) in fy_q_dict.items():
        quarters = find_quarter_rows(sheet_id, year_row)
        fy_q_dict[year][1] = {quarter.cells[0].value: quarter for quarter in quarters}
    return fy_q_dict


def find_fy_rows(sheet_id):
    fy_rows = []
    rows = smart.Sheets.get_sheet(sheet_id).rows
    for row in rows:
        if not row.to_dict().get('parentId', False):  # checks if row has a porent
            fy_rows.append(row)
    return fy_rows


def find_quarter_rows(sheet_id, year_row):
    q_rows = []
    rows = smart.Sheets.get_sheet(sheet_id).rows
    for row in rows:
        if row.to_dict().get('parentId', False) == year_row.id:  # checks if row's parent is the FY
            q_rows.append(row)
    return q_rows


def get_quarter_parent_id(fy, q, fy_q_dict):
    return fy_q_dict['FY' + str(fy)][1]['Q' + str(q)].id


if __name__ == '__main__':
    process_sheet(REQUEST_SHEET_ID, MAP_SHEET_ID, simulate=False)
