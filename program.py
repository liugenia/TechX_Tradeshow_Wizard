import smartsheet

from FY_Q_sort import calc_fy_q_hardcoded

smart = smartsheet.Smartsheet()  # use 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

REQUEST_SHEET_ID = 4026093033285508
MAP_SHEET_ID = 8844668382275460


def process_sheet(request_sheet_id: int,
                  map_sheet_id: int,
                  simulate: bool = False) -> None:
    """Main loop for processing the sheet

    takes the sheet ids for the request sheet to pull rows from, and
    the map sheet to send rows to. An optional simulate option does not
    alter any sheets, but only shows the rows that would be copied.

    Gets rows from the request sheet, and builds {name: id} column map

    Prints out the column names and ids

    For each row in the request sheet, the ETS status column is checked
    if it is Yellow, the row is printed and if simulation is false, the
    row is sent to the map sheet and then the ETS Status column is
    changed to green.

    Does not return anything.
    """

    rows = smart.Sheets.get_sheet(request_sheet_id).rows
    column_mapping = column_name_to_id_map(request_sheet_id)

    print_col_headings(column_mapping)

    for row in rows:
        if check_row(row, column_mapping):
            print_row(row, column_mapping)
            if not simulate:
                send_row(sheet_id=map_sheet_id,
                         row=row,
                         request_column_mapping=column_mapping)
                smart.Sheets.update_rows(request_sheet_id,
                                         update_row_status(row=row,
                                                           column_mapping=column_mapping,
                                                           color='Green'))
            else:
                print('Simulation! This row would have been updated to green and added to the map sheet.\n')


def send_row(sheet_id: int,
             row: smartsheet.models.Row,
             request_column_mapping: dict) -> None:
    """Main function for sending each row

    Takes the map sheet id, the row to be sent, and the request sheet
    {name: id} column map.

    Calculated the FY/Quarter number, thee map sheet {name: id}
    column map, and the dictionary of fy and quarter rows

    Creates an empty row, and sets the parent_id to the id of the
    quarter to which it belongs, and sets it to be added to the
    bottom of that row's children

    Iterates though all the cells, and if the name of that cell's
    column id is also in the map sheet, creates a new empty cell,
    copies over the value of the cell, sets the column id to be the
    column id that has the same name as the old cell's column, and
    appends that cell to the new row.

    Finally, that row is added to the map sheet

    Does not return anything.
    """

    fy, q = calc_fy_q_hardcoded(get_cell_by_column_name(row=row,
                                                        column_name='Event Start Date',
                                                        col_map=request_column_mapping).value)
    map_column_mapping = column_name_to_id_map(sheet_id)
    fy_q_dict = make_fy_q_dict(sheet_id, map_column_mapping)

    new_row = smartsheet.models.Row()
    new_row.parent_id = get_quarter_parent_id(fy, q, fy_q_dict)
    new_row.to_bottom = True

    for cell in row.cells:
        if reverse_dict_search(request_column_mapping, cell.column_id) in map_column_mapping.keys():
            new_cell = smartsheet.models.Cell()
            new_cell.value = cell.value
            new_cell.column_id = map_column_mapping[reverse_dict_search(request_column_mapping, cell.column_id)]
            new_row.cells.append(new_cell)
    update_row_status(row=new_row,
                      column_mapping=map_column_mapping,
                      column_name='ETS Status',
                      color='Green')
    smart.Sheets.add_rows(sheet_id, new_row)


def update_row_status(row: smartsheet.models.Row,
                      column_mapping: dict,
                      column_name: str = 'ETS Status',
                      color: str = 'Green') -> smartsheet.models.Row:
    """ Updates a row's ETS Status Column to Green

    Takes a row and a column mapping, and optionally the column name
    and value to change it to.

    Creates a new row object with the old row's id and cells, then
    changes the cell with the given column name to be the specified
    value

    Attempting to change the color to anything but one of the
    allowed_colors is an AssertionError and the original row is
    returned unchanged

    Otherwise, returns the new row object with the updated color column
    """

    allowed_colors = ['Red', 'Yellow', 'Green']
    new_row = smartsheet.models.Row()
    new_row.id, new_row.cells = row.id, row.cells
    try:
        assert color in allowed_colors
        get_cell_by_column_name(row, column_name, column_mapping).value = color
        return new_row
    except AssertionError:
        print(f"Color must be one of: {allowed_colors}. Color was {color}. Row will not be updated")
    return row


def check_row(row: smartsheet.models.Row,
              column_mapping: dict,
              column_name: str = 'ETS Status',
              val_to_test: str = 'Yellow') -> bool:
    return get_cell_by_column_name(row, column_name, column_mapping).value == val_to_test


def print_col_headings(cols: dict) -> None:  # prints the column name and id for all columns, plus FY/Quarter
    print(*(column_format(col_title) for col_title in cols.keys()), 'Start FY/Quarter')
    print(*(str(col_id).ljust(23) for col_id in cols.values()), end='\n\n')


def print_row(row: smartsheet.models.Row,
              column_mapping: dict,
              column_name: str = 'Event Start Date') -> None:
    # format, print the columns in the row + FY/Quarter
    print(*(column_format(cell.display_value or cell.value) for cell in row.cells), sep=' ', end=' ')
    fy, q = calc_fy_q_hardcoded(get_cell_by_column_name(row, column_name, column_mapping))
    print(f'FY{fy} Q{q}')


def column_format(item: str, just: int = 23) -> str:
    return (str(item)[:just - 2] + (str(item)[just - 2:] and '..')).ljust(just)


def column_name_to_id_map(sheet_id: int) -> dict:
    # returns a title:id dict of all columns in sheet
    return {column.title: column.id for column in smart.Sheets.get_columns(sheet_id, include_all=True).data}


def get_cell_by_column_name(row: smartsheet.models.Row,
                            column_name: str,
                            col_map: dict) -> smartsheet.models.Cell:
    return row.get_column(col_map[column_name])  # {NAME: ID}


def reverse_dict_search(search_dict: dict, search_value: str) -> str:
    for key, val in search_dict.items():
        if val == search_value:
            return key


def make_fy_q_dict(sheet_id: int,
                   column_mapping: dict,
                   column_name: str = 'Event Start Date') -> dict:
    fy_q_dict = {str(get_cell_by_column_name(fy,
                                             column_name,
                                             column_mapping).value): [fy, {}] for fy in find_fy_rows(sheet_id)}
    for year, (year_row, _) in fy_q_dict.items():
        quarters = find_quarter_rows(sheet_id, year_row)
        fy_q_dict[year][1] = {get_cell_by_column_name(quarter,
                                                      column_name,
                                                      column_mapping).value: quarter for quarter in quarters}
    return fy_q_dict


def find_fy_rows(sheet_id: int) -> list:
    fy_rows = []
    rows = smart.Sheets.get_sheet(sheet_id).rows
    for row in rows:
        if not row.to_dict().get('parentId', False):  # checks if row has a parent
            fy_rows.append(row)
    return fy_rows


def find_quarter_rows(sheet_id: int, year_row: smartsheet.models.Row) -> list:
    q_rows = []
    rows = smart.Sheets.get_sheet(sheet_id).rows
    for row in rows:
        if row.to_dict().get('parentId', False) == year_row.id:  # checks if row's parent is the FY
            q_rows.append(row)
    return q_rows


def get_quarter_parent_id(fy: int, q: int, fy_q_dict: dict) -> int:
    return fy_q_dict['FY' + str(fy)][1]['Q' + str(q)].id


if __name__ == '__main__':
    process_sheet(REQUEST_SHEET_ID, MAP_SHEET_ID, simulate=False)
