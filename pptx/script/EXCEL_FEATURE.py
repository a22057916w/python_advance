import pandas as pd
import numpy as np

class Workbook():

    def __init__(self, path = None):
        country = pd.read_excel(path, sheet_name="Post-RTS", skiprows=1)

        df_postRTS = self.truncate_df(country, "P-RTS Country (Voluntary):", 0)
        #print(df_postRTS)
        df_postRTS = self.drop_na_row(df_postRTS)
        print(df_postRTS)

    def truncate_df(self, df, str_value, n_col, *, first_row = 0):
        last_row = -1

        row = df.shape[0]   # return df row number
        for i in range(row):
            if df.iloc[i, n_col] == str_value:
                last_row = i - 1    # don't need the row we found
                break

        return df.truncate(before=first_row, after=last_row)

    def drop_na_row(self, df):
        b_allna = False

        drop_list = []

        row = df.shape[0]
        for i in range(row):
            s = pd.Series(df.iloc[i, :])
            if s.isnull().sum() == len(df.columns):
                drop_list.append(i)

        return df.drop(drop_list)
