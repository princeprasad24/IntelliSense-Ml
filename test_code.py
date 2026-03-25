# from datetime import datetime
# import time


# prev_timestamp = datetime.now().strftime("%H:%M:%S")
# print(prev_timestamp)

# print("Sleeping")
# time.sleep(10)

# timestamp = datetime.now().strftime("%H:%M:%S")
# print(timestamp)


# prev_time = datetime.strptime(prev_timestamp, "%H:%M:%S")
# curr_time = datetime.strptime(timestamp, "%H:%M:%S")

# deff = (curr_time) - prev_time

# print(deff)
# print(deff.total_seconds())
# print(datetime.strftime(curr_time , "%H:%M:%S"))
# print(type(curr_time))

link = "https://final-year-project-abedc-default-rtdb.asia-southeast1.firebasedatabase.app/State.json"
import requests


data = requests.get(link);

print(data.content)
state_data = {"Water Pump":"ON","bulb":"ON","pump":"ON"}


sent_data = requests.put(link,json=state_data)
updated_data = requests.get(link)


print(updated_data.content)