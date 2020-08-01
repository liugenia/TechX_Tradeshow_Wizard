import smartsheet

from program import find_fy_rows, find_quarter_rows

smart = smartsheet.Smartsheet()  # use 'SMARTSHEET_ACCESS_TOKEN' env variable
smart.errors_as_exceptions(True)

TEST_MAP_SHEET_ID = 8844668382275460

info = smart.Server.server_info()

for year_row in find_fy_rows(TEST_MAP_SHEET_ID):
    for quarter_row in find_quarter_rows(TEST_MAP_SHEET_ID, year_row):
        new_row = smartsheet.models.Row(dict(id=quarter_row.id,
                                             cells=quarter_row.cells))

        for cell in new_row.cells:
            cell.format = ',,,,,,,,,25,,,,,,'
            if not cell.value:
                cell.value = ''
        new_row.format = ',,,,,,,,,25,,,,,,'

        smart.Sheets.update_rows(TEST_MAP_SHEET_ID, new_row)

    new_row = smartsheet.models.Row(dict(id=year_row.id,
                                         cells=year_row.cells))

    for cell in new_row.cells:
        cell.format = ',,,,,,,,,30,,,,,,'
        if not cell.value:
            cell.value = ''
    new_row.format = ',,,,,,,,,30,,,,,,'

    smart.Sheets.update_rows(TEST_MAP_SHEET_ID, new_row)
