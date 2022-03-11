import pandas as pd
import numpy as np

class DataFrameFeature():

    # truncate df according to the value in given column
    @staticmethod
    def truncate(df, *, column, first_value, last_value):
        first_row = last_row = -1
        n_col = column

        b_first = False

        row = df.shape[0]   # return df row number
        for i in range(row):

            if df.iloc[i, n_col] == first_value:
                b_first = True
                first_row = i + 1

            if last_value == None and pd.isna(df.iloc[i, n_col]):
                #print(i)
                last_row = i - 1
                #print(df.iloc[i, :])
            elif df.iloc[i, n_col] == last_value:
                last_row = i - 1    # we don't need the row we found

            if b_first and first_row < last_row:
                #print(first_row, last_row)
                #print("sdfsdfs")
                break

        return df.truncate(before=first_row, after=last_row).reset_index(drop=True)

    # drop row that has NaN in each column
    @staticmethod
    def drop_na_row(self, df):
        drop_list = []

        row = df.shape[0]
        for i in range(row):
            s = pd.Series(df.iloc[i, :])    # trun df column into Series

            # if all column value is NaN, drop the row
            if s.isnull().sum() == len(df.columns):
                drop_list.append(i)

        return df.drop(drop_list).reset_index(drop=True)

    @staticmethod
    def drop_row(self, df, idx):
        return df.drop(idx).reset_index(drop=True)
