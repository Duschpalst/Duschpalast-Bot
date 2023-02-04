"""from datetime import date, timedelta

day = date.today()
name = []
for x in range(14):
    days = day - timedelta(days=x)
    if days == day:
        name.append("Heute")
    elif days == (day - timedelta(days=1)):
        name.append("Gestern")
    else:
        name.append(f"{days.day}.{days.month}.{days.year}")

    print(name)
"""
from ast import literal_eval

tmp = '[["1.1.2023", "Verwarnung Ⅰ", "Das und das"], ["2.2.2023", "Verwarnung Ⅱ", "Dies und das"]]'
tmp = literal_eval(tmp)
print(tmp)

tmp.append(["3.2.2023", "Verwarnung Ⅱ", "Dies und dies"])

print(tmp)