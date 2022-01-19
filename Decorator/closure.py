def student():
    height = 170
    weight = 60
    def info():
        print("my height is {}.".format(height))
        print("my weight is {}.".format(weight))
    return info
print(student)
print(student())
print("---------------------------")
students = student()
students()

"""
一般情況下，function中內區域變數的生命週期(life cycle)會隨著function執行完畢而結束(變數的生命週期在這篇文章有提到)，但是print出來的結果卻還可以讀取到height、weight兩個屬於student()scope的變數
"""
