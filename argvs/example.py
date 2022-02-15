
# The *args will give you all function parameters as a tuple:
def foo(*args):
    for a in args:
        print(a)

foo(14546)

foo(1,2,3,4,5,6,7,8,20)

print("\n*******************")

# The **kwargs will give you all keyword arguments except for those corresponding to a formal parameter as a dictionary.
def bar(**kwargs):
    for a in kwargs:
        print(a, kwargs[a])

bar(name='one', age=27)
# name one
# age 27
bar(x=3, y=4, life="mess")
#print(type({"god" : False, "pay" : "poor"}))
# can not take dict as argument
bar(god=False, pay="poor")


# parameter keyword name must equal to argument keyword name
def fuck(arg1, arg2, arg3, *, a, god=False):
    print(arg1)
    print(arg2)
    print(arg3)

    print(a)
    print(god)
    # for e in b:
    #     print(b)

fuck(1, 2, 3, a="sdfsdf")
