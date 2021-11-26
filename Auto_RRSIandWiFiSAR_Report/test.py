import os, time

dir = "./test_SN"
for file in os.listdir(dir):
    print(file)
    c_time = os.path.getctime(os.path.join(dir, file))
    local_time = time.ctime(c_time)
    print(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(c_time)))
