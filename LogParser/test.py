import re

text = 'DUT return: AT#TESTMODE="CH3G 9750"'

print(re.search(r'"CH(.*) [0-9]*"', text).group(0))
dict1 = {}
dict2 = {}
dict1["a"] = 2
dict2["b"] = 3
dict1.update(dict2)
print(dict1)
