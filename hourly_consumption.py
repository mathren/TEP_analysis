import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime as dt


def read_data(fname):
    """
    fname: string with path to csv downloaded from TEP website
    returns lists
    """
    date = []
    t_start = []
    t_end = []
    consumption = []  # in KWh
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            if i <= 2: continue  # skip header
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


def sunday_formatter(x, pos):
    """Custom formatter to display labels only for Sundays."""
    date = mdates.num2date(x)
    return date.strftime('%d %b') if date.weekday() == 6 else ""


if __name__ == "__main__":
    # put in this folder the csv file name and change the string below
    fname = './HourlyIntervalData-20240621_20241111.csv'
    date, t_start, t_end, consumption = read_data(fname)
    fixed_dates = convert_dates(date, t_start)
    fig, ax = plt.subplots(figsize=(16, 9))
    bx = ax.twinx()
    consumption = np.array(consumption, dtype=float)
    ax.plot(fixed_dates, consumption, lw=1)
    bx.plot(fixed_dates, np.cumsum(consumption), lw=3, c='C1', zorder=1)
    ax.scatter(fixed_dates, np.array(consumption, dtype=float))
    # add markers
    # ax.axhline(avg_production(), c='r', lw=3, zorder=0, label)
    ax.axhline(8.17, c='r', ls="-.", zorder=0, label=r"Net Zero Solar Production")
    ax.axvline(convert_one_date_time("07/21/2024", "1:00 AM"), 0, 1, ls='--', c='blue')
    ax.axvline(convert_one_date_time("08/10/2024", "1:00 AM"), 0, 1, ls='--', c='purple')
    ax.set_ylabel(r'Hourly Consumption [KWh]')
    ax.set_xlabel(r'Date')
    bx.set_ylabel(r'Cumulative consumption [Kwh]', color='C1')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=6))  # Major ticks on Sundays
    ax.xaxis.set_minor_locator(mdates.DayLocator())  # Minor ticks every day
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sunday_formatter))
    # Rotate and align the labels for better readability
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    bx.tick_params(colors="C1", which="both")
    bx.spines['right'].set_color("C1")
    # ax.legend()
    ax.text(0.05, 0.9, r"Prop. 2 production", size=20,
            color='red', transform=ax.transAxes, ha='left', va='center')
    plt.savefig("consumption.pdf")
    plt.show()
