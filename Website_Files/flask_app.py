from flask import Flask, render_template, url_for
import json
from datetime import datetime
import os
import time

app = Flask(__name__)

os.environ["TZ"] = "America/New_York"
time.tzset()


@app.route("/")
def welcome():
    return "Welcome to the Improv Newsletter"


with open("improv/templates/wiki_data_bdays.json", "r") as fp:
    bdays = json.load(fp)

with open("improv/templates/wiki_data_ddays.json", "r") as fp:
    ddays = json.load(fp)

with open("improv/templates/news_dump.json", "r") as fp:
    news_data = json.load(fp)

days_with_b = []
for k, v, in bdays.items():
    if v['full_day'] not in days_with_b:
        days_with_b.append(v['full_day'])
    else:
        pass

days_with_b_dict = {}
for k, v, in bdays.items():
    full = v['full_day']
    if full not in days_with_b_dict:
        days_with_b_dict[full] =  v['month_day']
    else:
        pass

days_with_d_dict = {}
for k, v, in ddays.items():
    full = v['full_day']
    if full not in days_with_d_dict:
        days_with_d_dict[full] =  v['month_day']
    else:
        pass

days_with_d = []
for k, v, in ddays.items():
    if v['full_day'] not in days_with_d:
        days_with_d.append(v['full_day'])
    else:
        pass

today = datetime.today()
month_name = today.strftime("%B")
day_name = today.strftime("%A")
today_num_str = str(today.day)
today_num_int = int(today.day)

@app.route("/newsletter")
def newsletter():
    week = day_name + ", " + month_name + " " + today_num_str
    return render_template('newsletter.html', week=week, bdays=bdays, days_with_b=days_with_b, days_with_b_dict=days_with_b_dict, days_with_d_dict=days_with_d_dict,
                            days_with_d=days_with_d, news_data=news_data, ddays=ddays, today_num_int=today_num_int)



if __name__ == "__main__":
    app.run()

