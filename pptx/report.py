import os
import pandas as pd


import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches

class PptxReport():
    def __init__(self, df):
        self.prs = Presentation()
        self.df = df

        self.outputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")

    def run(self):
        self.create_table(df)
        self.prs.save(self.outputPath)

    def create_table(self, df):
        blank_slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(blank_slide_layout)
        shapes = slide.shapes

        #shapes.title.text = "Fuck this shit"

        left = top = Inches(0)
        width = Inches(5)
        height = Inches(2)

        rows = df.shape[0] + 1
        cols = df.shape[1]
        #print(rows, cols)
        table = shapes.add_table(rows, cols, left, top, width, height).table

        for col in range(df.shape[1]):
            table.columns[col].height = Inches(2.0)
            #table.cell(0, col).text = str(df.columns[col])
            for row in range(df.shape[0] + 1):
                if row == 0:
                    table.cell(row, col).text = str(df.columns[col])
                    continue
                table.cell(row, col).text = str(df.iloc[row - 1, col])



if __name__ == "__main__":
    df = pd.read_excel("./data/test.xlsx")

    # prs = Presentation()
    # title_only_slide_layout = prs.slide_layouts[5]
    print(df)
    print(df.iloc[1, 1])
    print(len(df.iloc[:, 0]))
    print(df.shape[0] + 1)
    print(df.columns[0])

    PR = PptxReport(df)
    PR.run()

    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
