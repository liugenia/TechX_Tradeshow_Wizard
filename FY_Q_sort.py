from datetime import date, datetime

QUARTER = 13 * 7
FISCAL_YEAR = QUARTER * 4
FY20_Q1_START = date(2019, 7, 28)

YEARS_AND_QUARTERS = {
    20: {
        1: (date(2019, 7, 28), date(2019, 10, 26)),
        2: (date(2019, 10, 27), date(2020, 1, 25)),
        3: (date(2020, 1, 26), date(2020, 4, 25)),
        4: (date(2020, 4, 26), date(2020, 7, 25))
        },
    21: {
        1: (date(2020, 7, 26), date(2020, 10, 24)),
        2: (date(2020, 10, 25), date(2021, 1, 23)),
        3: (date(2021, 1, 24), date(2021, 5, 1)),
        4: (date(2021, 5, 2), date(2021, 7, 31))
        }
    }


def calc_fy_q(input_date):
    input_date = datetime.strptime(input_date, '%m/%d/%y')
    input_date = date(input_date.year, input_date.month, input_date.day)
    delta = (input_date-FY20_Q1_START).days
    fy = delta // FISCAL_YEAR
    q = delta % FISCAL_YEAR // QUARTER
    return 20 + fy, q + 1


def calc_fy_q_hardcoded(input_date):
    input_date = datetime.strptime(input_date, '%m/%d/%y').date()
    for year, quarters in YEARS_AND_QUARTERS.items():
        for quarter, time_range in quarters.items():
            if time_range[0] <= input_date <= time_range[1]:
                return year, quarter
    else:
        return 0, 0


def print_quarters():
    for year, quarters in YEARS_AND_QUARTERS.items():
        print(f'FY{year}:')
        for quarter, time_range in quarters.items():
            print(f'\tQ{quarter}:')
            print(f'\t\ttime range: {time_range[0]} – {time_range[1]}')
            print(f'\t\tduration: {(time_range[1]-time_range[0]).days}')


if __name__ == '__main__':
    test_dates = ['04/20/17', '01/01/20', '07/22/20', '07/27/20', '07/31/21', '10/08/21']

    for test_date in test_dates:
        print(test_date)
        # first test - calculate quarter using beginning of FY20. Problem: FY21 Q3 has an extra week, which messes it up
        result = calc_fy_q(test_date)
        print('test1 1:\n\t', result)
        print(f'\tFY{result[0]} Q{result[1]}')
        # second test - calculate quarter from a hardcoded list of quarters with start/end dates
        result = calc_fy_q_hardcoded(test_date)
        print('test1 1:\n\t', result)
        print(f'\tFY{result[0]} Q{result[1]}\n')

    # just print all the years and quarters
    print_quarters()
