import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date as date_class
from datetime import timedelta, datetime
from matplotlib.ticker import PercentFormatter

df = pd.read_csv(r'/home/anto/Documents/Coding/fred_graph/data_27_05_2021.csv')
# plot original data from FRED
df = df[df.RRPONTSYD != "."]
X = [dt.datetime.strptime(value[0], "%Y-%m-%d") for value in df.values]
Y = [float(value[1]) for value in df.values]

def get_quarter(p_date: date_class) -> int:
    return (p_date.month - 1) // 3 + 1


def get_first_day_of_the_quarter(p_date: date_class):
    return datetime(p_date.year, 3 * ((p_date.month - 1) // 3) + 1, 1)


def get_last_day_of_the_current_quarter(p_date: date_class):
    quarter = get_quarter(p_date)
    cq =  datetime(p_date.year + 3 * quarter // 12, 3 * quarter % 12 + 1, 1) + timedelta(days=-1)
    while cq not in X:
        try:
            # while this is not a trading day, check if previous day is a trading day
            cq = datetime(cq.year,cq.month, cq.day-1)
        except:
            # if we don't have the info for that month, it is too far in the future. 
            # In that case, return 9999,1,1 as convention
            cq = datetime(9999,1,1)
            break
    return cq


def get_last_day_of_the_previous_quarter(p_date: date_class):
    pq = None
    if p_date.month < 4:
        pq = datetime(p_date.year - 1, 12, 31)
    elif p_date.month < 7:
        pq = datetime(p_date.year, 3, 31)
    elif p_date.month < 10:
        pq = datetime(p_date.year, 6, 30)
    else:
        pq = datetime(p_date.year, 9, 30)
    
    while pq not in X:
        try:
            pq = datetime(pq.year,pq.month,pq.day-1)
        except:
            # If error (shouldn't happen in theory)
            pq = datetime(1,1,1)
            break
    return pq


def get_closest_end_of_quarter(p_date: date_class):
    #current quarter / previous quarter
    cq = get_last_day_of_the_current_quarter(p_date)
    pq = get_last_day_of_the_previous_quarter(p_date)
    #distance current quarter/previous quarter
    d_cq = cq-p_date
    d_pq = p_date-pq
    #return closest end of quarter
    if d_cq < d_pq:
        return cq
    else:
        return pq



# fill eoq_data with dict containing { datetime(eoq_date) : price }
eoq_data = {}
for date_price in df.values:
    curr_date = datetime.strptime(date_price[0], "%Y-%m-%d")
    cq = get_last_day_of_the_current_quarter(curr_date) # cq = current quarter
    if curr_date == cq:
        eoq_data[curr_date] = float(date_price[1])
    elif cq == datetime(9999,1,1) or cq == datetime(1,1,1):
        # data of current quarter not available
        pass 

data = df.copy(deep=True)
data = data.values
data = dict((datetime.strptime(value[0], "%Y-%m-%d"), float(value[1])) for value in data )

""" # it would probably be better just not to print these sections
 for d in data:
    if data[d] < 1.0 and d in eoq_data:
        print(f"{d} : {eoq_data[d]}")
        # if eoq is less than 1, you might get some funny percentages :)
        data[d] = 10 """

data_in_percentage = {}
for date in data:
    csq = get_closest_end_of_quarter(date) # csq = closest end of quarter
    if csq == datetime(9999,1,1):
        # data of current quarter not available
        break
    else:
        if data[csq] > 25:
            data_in_percentage[date] = round(data[date]/data[csq],2)
        
    
# plot data in percentage relative to peak (closest quarter end)

X_percentage = [d for d in data_in_percentage]
Y_percentage = [data_in_percentage[d] for d in data_in_percentage]

plt.plot(X_percentage, Y_percentage)
plt.xlabel("date")
plt.gcf().autofmt_xdate()
plt.ylabel("Percentage of reverse repo relative to nearest end of quarter")
plt.title("Overnight Reverse Repurchase Agreements In Percentage relative to closest EOQ")
plt.show()


