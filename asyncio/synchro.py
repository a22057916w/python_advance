import time

start_time = time.time()

def sleep_sec(sec):
    print('start at: ', time.time() - start_time)
    time.sleep(sec)
    print('end at: ', time.time() - start_time)


def main():
    for i in range(5):
        sleep_sec(1)
    print('end of main: ', time.time() - start_time)

main()
