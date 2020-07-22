import datetime

QUARTER = 13 * 7
FISCAL_YEAR = QUARTER * 4
FY20_Q1_START = datetime.date(2019, 7, 28)

QUARTERS = {
    20: {
        1: (datetime.date(2019, 7, 28), datetime.date(2019, 10, 26)),
        2: (datetime.date(2019, 10, 27), datetime.date(2020, 1, 25)),
        3: (datetime.date(2020, 1, 26), datetime.date(2020, 4, 25)),
        4: (datetime.date(2020, 4, 26), datetime.date(2020, 7, 25))
        },
    21: {
        1: (datetime.date(2020, 7, 26), datetime.date(2020, 10, 24)),
        2: (datetime.date(2020, 10, 25), datetime.date(2021, 1, 23)),
        3: (datetime.date(2021, 1, 24), datetime.date(2021, 5, 1)),
        4: (datetime.date(2021, 5, 2), datetime.date(2021, 7, 31))
        }
    }


def calc_fy_q(input_date):
    input_date = datetime.datetime.strptime(input_date, '%m/%d/%y')
    input_date = datetime.date(input_date.year, input_date.month, input_date.day)
    delta = (input_date-FY20_Q1_START).days
    fy = delta // FISCAL_YEAR
    q = delta % FISCAL_YEAR // QUARTER
    return 20 + fy, q + 1


def calc_fy_q_hardcoded(input_date):
    input_date = datetime.datetime.strptime(input_date, '%m/%d/%y').date()
    for year, quarters in QUARTERS.items():
        for quarter, time_range in quarters.items():
            if time_range[0] <= input_date <= time_range[1]:
                return year, quarter


def print_quarters():
    for year, quarters in QUARTERS.items():
        print(f'FY{year}:')
        for quarter, time_range in quarters.items():
            print(f'\tQ{quarter}:')
            print(f'\t\ttime range: {time_range[0]} – {time_range[1]}')
            print(f'\t\tduration: {(time_range[1]-time_range[0]).days}')


if __name__ == '__main__':
    test_date = '07/31/21'

    # first test - calculate quarter from the beginning of FY20. Problem: FY21 Q3 has an extra week, which messes it up
    print(calc_fy_q(test_date))

    # second test - calculate quarter from a hardcoded list of quarters with start/end dates
    result = calc_fy_q_hardcoded(test_date)
    print(result)
    print(f'FY{result[0]} Q{result[1]}')

    # just print all the years and quarters
    print_quarters()
