import pandas as pd
import numpy as np

arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue'], ["a", "b", "c", "d"]]

mutil_index = pd.MultiIndex.from_arrays(arrays)
print(mutil_index)

df = pd.DataFrame(np.random.randn(8, 4), columns=mutil_index)
print(df)
