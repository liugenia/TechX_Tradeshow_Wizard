import smartsheet


year_row_color_index = 21
quarter_and_event_colors = [(12, 5),
                            (14, 7),
                            (15, 8),
                            (16, 9)]


def colorize_rows(smart: smartsheet.Smartsheet, sheet_id: int) -> None:
    from program import find_child_rows, find_fy_rows
    rows_to_update = []
    for year_row in find_fy_rows(sheet_id):
        for i, quarter_row in enumerate(find_child_rows(sheet_id, year_row.id)):
            for event_row in find_child_rows(sheet_id, quarter_row.id):
                new_row = smartsheet.models.Row(dict(id=event_row.id,
                                                     cells=event_row.cells))

                for cell in new_row.cells:
                    cell.format = f',,,,,,,,,{quarter_and_event_colors[i][1]},,,,,,'
                    if not cell.value:
                        cell.value = ''
                new_row.format = f',,,,,,,,,{quarter_and_event_colors[i][1]},,,,,,'
                rows_to_update.append(new_row)

            new_row = smartsheet.models.Row(dict(id=quarter_row.id,
                                                 cells=quarter_row.cells))

            for cell in new_row.cells:
                cell.format = f',,,,,,,,,{quarter_and_event_colors[i][0]},,,,,,'
                if not cell.value:
                    cell.value = ''
            new_row.format = f',,,,,,,,,{quarter_and_event_colors[i][0]},,,,,,'
            rows_to_update.append(new_row)

        new_row = smartsheet.models.Row(dict(id=year_row.id,
                                             cells=year_row.cells))

        for cell in new_row.cells:
            cell.format = f',,,,,,,,,{year_row_color_index},,,,,,'
            if not cell.value:
                cell.value = ''
        new_row.format = f',,,,,,,,,{year_row_color_index},,,,,,'
        rows_to_update.append(new_row)
    smart.Sheets.update_rows(sheet_id, rows_to_update)
