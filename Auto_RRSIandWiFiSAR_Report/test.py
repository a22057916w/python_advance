import os, time
import datetime as df

dir = "./test_SN"
for file in os.listdir(dir):
    print(file)
    c_time = os.path.getctime(os.path.join(dir, file))
    local_time = df.datetime.fromtimestamp(c_time)
    print(local_time.strftime("%Y-%m-%d %H:%M:%S"))

test_time = df.datetime.strptime("2021-11-27 13:13:13", "%Y-%m-%d %H:%M:%S")
print(type(test_time), type(local_time))
if test_time > local_time:
    print(test_time)
else:
    print(local_time.strftime("%Y-%m-%d %H:%M:%S"))
