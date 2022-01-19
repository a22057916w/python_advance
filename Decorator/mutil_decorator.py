def print_func_name(func):
    def warp_1():
        print("Now use function '{}'".format(func.__name__))
        func()
    return warp_1


def print_time(func):
    import time
    def warp_2():
        print("Now the Unix time is {}".format(int(time.time())))
        func()
    return warp_2


@print_func_name
@print_time
def dog_bark():
    print("Bark !!!")



if __name__ == "__main__":
    dog_bark()
    # > Now use function 'warp_2'
    # > Now the Unix time is 1541239747
    # > Bark !!!

"""
decorators 多層的話是採 ”recursive” 的方式處理，如果一個 function 有兩個以上的 decorators ，邏輯上則會先合併「最靠近」的 decorator 吐出新的 function 再由上面一個的 decorator 吃進去！
"""