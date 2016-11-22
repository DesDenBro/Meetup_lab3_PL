def GetNormalDatetime(secs):
    # время в миллисекундах, а нужно в секундах, делим secs на 1000
    return dt.datetime.strptime((time.ctime(secs / 1000)), "%a %b %d %H:%M:%S %Y")

def CombineRequest():
    global country, city, key, topic
    return "https://api.meetup.com/2/open_events?" \
            + "key=" + key \
            + "&photo-host=public&" \
            + "country=" + country + "&" \
            + "topic=" + topic + "&" \
            + "city=" + city + "&" \
            + "page=20"

import requests
import json
import time
import datetime as dt
country = "ru"          # страна
city = "moscow"         # город
topic = "softwaredev"   # тематика
key = '1f154302966384560a70115e547465'
oneweek = dt.datetime.utcnow() + dt.timedelta(days=7)

result = requests.get(CombineRequest())
parse_str = json.loads(result.text)

file = open("events.html", "w+", encoding='utf-8')
for event in parse_str["results"]:
    # Если событие в пределах недели от времени запуска программы
    if oneweek > GetNormalDatetime(event["time"]):
        file.write("<h2 align='center' style='color: blue'><a href=" + event["event_url"] + ">"
                   + event["name"] + "</a></h2>")
        if 'venue' in event:
            file.write("<h3 align='center'> Адрес: " + event["venue"]["address_1"] + "</h3>")
        file.write("<h3 align='center'> Время начала (UTC): "
                   + str(GetNormalDatetime(event["time"]))
                   + "</h3>")
        file.write(event["description"])

