import pandas as pd

pm10 = pd.read_csv("./cleaned_MKE_2020_pm10.csv")

so2 = pd.read_csv("./cleaned_MKE_2020_so2.csv")

pm25 = pd.read_csv("./split_0_8765.csv")


files = [pm10, so2, pm25]
names = ["pm10", "so2", "pm25"]
hoursoutput = {}


for df, name in zip(files, names):
    missing_hours = 0
    for i in range(1, len(df)):
        hour_diff = int(df.iloc[i]['Time Local'].split(":")[0]) - int(df.iloc[i-1]['Time Local'].split(":")[0])
        
        if hour_diff != 1 and hour_diff != -23:
            missing_hours += abs(hour_diff) - 1
    hoursoutput[name] = missing_hours

print("Missing Hours: ", hoursoutput)

from datetime import datetime

def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%y'): 
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
        
daysoutput = {}

for df, name in zip(files, names):
    missing_days = 0
    previous_date = parse_date(df.iloc[0]['Date Local'])
    for i in range(1, len(df)):
        current_date = parse_date(df.iloc[i]['Date Local'])
        day_difference = (current_date - previous_date).days
        if day_difference > 1:
            missing_days += day_difference - 1
            print(name, current_date, previous_date, day_difference -1)
        previous_date = current_date
    
    daysoutput[name] = missing_days

print("Missing Days: ", daysoutput)
