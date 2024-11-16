import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def read_data(fname):
    date = []
    t_start = []
    t_end = []
    consumption = []  # in KWh
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            if i <= 2: continue
            line = line.split(',')
            date.append(line[-6])
            t_start.append(line[-5])
            t_end.append(line[-4])
            consumption.append(line[-3])
    return date, t_start, t_end, consumption


def convert_one_date_time(one_date, t_start=""):
    # add 30 min to center hour
    t_start = t_start.replace(":00", ":30")
    string = one_date+" - "+t_start
    return np.datetime64(dt.datetime.strptime(string, '%m/%d/%Y - %I:%M %p'))


def convert_dates(date, t_start):
    x = []
    for i in range(len(date)):
        x.append(convert_one_date_time(date[i], t_start[i]))
    return np.array(x)


def avg_production(annual_production=14800):  # Kwh/yr
    daily_production = annual_production / 365.0
    hourly_production = daily_production / 12.0  # estimate 12h of Sun
    return hourly_production  # KWh


if __name__ == "__main__":
    date, t_start, t_end, consumption = read_data('./HourlyIntervalData-20240621_20241111.csv')
    fixed_dates = convert_dates(date, t_start)
    fig, ax = plt.subplots()
    ax.plot(fixed_dates, np.array(consumption, dtype=float), lw=1)
    ax.scatter(fixed_dates, np.array(consumption, dtype=float))
    # add markers
    ax.axhline(avg_production(), c='r', lw=3, zorder=0)
    ax.axvline(convert_one_date_time("07/21/2024", "1:00 AM"), 0, 1, ls='--', c='blue')
    ax.axvline(convert_one_date_time("08/10/2024", "1:00 AM"), 0, 1, ls='--', c='purple')
    ax.set_ylabel(r'Hourly Consumption [KWh]')
    ax.set_xlabel(r'Date')
    plt.show()
    # plt.savefig("consumption.pdf")