import smartsheet

from program import find_event_rows, find_fy_rows, find_quarter_rows

year_row_color_index = 21
quarter_and_event_colors = [(12, 5),
                            (14, 7),
                            (15, 8),
                            (16, 9)]


def colorize_rows(smart: smartsheet.Smartsheet, sheet_id: int) -> None:
    for year_row in find_fy_rows(sheet_id):
        print('Year')
        for i, quarter_row in enumerate(find_quarter_rows(sheet_id, year_row)):
            print(f'    Quarter{i+1}')
            for event_row in find_event_rows(sheet_id, quarter_row.id):
                print('        Event')
                new_row = smartsheet.models.Row(dict(id=event_row.id,
                                                     cells=event_row.cells))

                for cell in new_row.cells:
                    cell.format = f',,,,,,,,,{quarter_and_event_colors[i][1]},,,,,,'
                    if not cell.value:
                        cell.value = ''
                new_row.format = f',,,,,,,,,{quarter_and_event_colors[i][1]},,,,,,'
                smart.Sheets.update_rows(sheet_id, new_row)

            new_row = smartsheet.models.Row(dict(id=quarter_row.id,
                                                 cells=quarter_row.cells))

            for cell in new_row.cells:
                cell.format = f',,,,,,,,,{quarter_and_event_colors[i][0]},,,,,,'
                if not cell.value:
                    cell.value = ''
            new_row.format = f',,,,,,,,,{quarter_and_event_colors[i][0]},,,,,,'
            smart.Sheets.update_rows(sheet_id, new_row)

        new_row = smartsheet.models.Row(dict(id=year_row.id,
                                             cells=year_row.cells))

        for cell in new_row.cells:
            cell.format = f',,,,,,,,,{year_row_color_index},,,,,,'
            if not cell.value:
                cell.value = ''
        new_row.format = f',,,,,,,,,{year_row_color_index},,,,,,'
        smart.Sheets.update_rows(sheet_id, new_row)
