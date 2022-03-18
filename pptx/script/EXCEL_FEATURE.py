import pandas as pd
import numpy as np

import openpyxl
from openpyxl import load_workbook

class DataFrameFeature():
    _NaN = "NaN"  # represent the NaN value in df

    # filter column values by remove string behind "sep", and r-strip space
    @staticmethod
    def filter_column_value(df, *, column_name, sep):
        col = df.columns.get_loc(column_name)   # get col_idx by col_name

        for row in range(df.shape[0]):
            value = df.iloc[row, col]

            # if the country value is Nan, do nothing
            if pd.isna(value):
                continue

            sep_idx = value.find(sep)   # find character "sep" in given string

            # if not found the target sep, right strip space only, else cut the string behind sep
            if sep_idx == -1:
                df.iloc[row, col] = value.rstrip(" ")
            else:
                df.iloc[row, col] = value[:sep_idx].rstrip(" ")
        #return df

    @staticmethod
    def get_country_set(df, *, category):
        list_ctry = []
        total_ctry = 0

        col_ctry = df.columns.get_loc("Country")
        col_ctgy = df.columns.get_loc("Category")
        col_cert = df.columns.get_loc("Certificate")

        for row in range(df.shape[0]):
            ctry = df.iloc[row, col_ctry]
            ctgy = df.iloc[row, col_ctgy]
            cert = df.iloc[row, col_cert]

            if pd.isna(ctgy):
                continue

            if category == ctgy:
                if pd.isna(ctry):
                    continue
                elif ctry.find("/") != -1:
                    list_ctry.append(ctry + "(" + cert + ")")
                    total_ctry += len(ctry.split("/"))
                else:
                    list_ctry.append(ctry + "(" + cert + ")")
                    total_ctry += 1

        return total_ctry, list_ctry

    # truncate df according to the value in given column
    @staticmethod
    def truncate(df, *, column, first_value, last_value):
        first_row = last_row = -1
        n_col = column

        b_first = False     # make sure we found the first_value as flag

        row = df.shape[0]   # return df row number
        for i in range(row):
            if df.iloc[i, n_col] == first_value:
                b_first = True
                first_row = i + 1   # we don't need the row we found

            # check if last_value is NaN or not
            if last_value == DataFrameFeature.NaN and pd.isna(df.iloc[i, n_col]):
                last_row = i - 1
            elif df.iloc[i, n_col] == last_value:
                last_row = i - 1    # we don't need the row we found

            if b_first and first_row < last_row:
                break

        # reset index order after truncated
        return df.truncate(before=first_row, after=last_row).reset_index(drop=True)

    # drop row that has NaN in each column
    @staticmethod
    def drop_na_row(df):
        drop_list = []

        # find rows with NaN in each column
        row = df.shape[0]
        for i in range(row):
            s = pd.Series(df.iloc[i, :])    # trun df column into Series

            # if all column value is NaN, drop the row
            if s.isnull().sum() == len(df.columns):
                drop_list.append(i)

        return df.drop(drop_list).reset_index(drop=True)

    @staticmethod
    def drop_row(df, idx):
        return df.drop(idx).reset_index(drop=True)

    @property
    def NaN(self):
        return self._NaN



class WorkBookFeature():
    def __init__(self, path):
        self.wb = load_workbook(filename=path)
        print(self.get_cell_value(sheetname="RF Schedule DVT2", str_pos="D3"))

    def get_cell_value(self, *, sheetname, str_pos):
        return self.wb[sheetname][str_pos].value

    def get_WWAN_ID():
        pass
