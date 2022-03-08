import openpyxl


class Country():

    def __init__(self, workbook):
        self.country = []
        self.set_country(workbook)

    def set_country(self, workbook):
        ws = workbook["Post-RTS"]
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=4, max_col=7):

            # init the data that need to store as dict
            ctry = {
                "name": "na",
                "certificate": "na",
                "schedule": "na"
            }

            # set dict value form col 4, 5, 7, respectively row[0], [1], [3]
            ctry["name"] = row[0].value if row[0].value != None else "na"
            ctry["certificate"] = row[1].value if row[1].value != None else "na"
            ctry["schedule"] = row[3].value if row[3].value != None else "na"
            print(ctry["name"])
            self.country.append(ctry)

    # count the number of country name
    def count(self):
        temp_list = []
        #print(self.country)
        for info in self.country:
            if info["name"] not in temp_list:
                temp_list.append(info["name"])
        print(temp_list)
        return len(temp_list)

class Workbook():

    def __init__(self, workbook = None):
        self.workbook = workbook
        self.country = Country(workbook)
        print(self.country.count())
