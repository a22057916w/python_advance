import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
title_only_slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(title_only_slide_layout)
shapes = slide.shapes

shapes.title.text = "Adding a Table"

rows = cols = 2
left = top = Inches(2)
width = Inches(6)
height = Inches(6)


table = shapes.add_table(rows, cols, left, top, width, height).table

table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(20.0)

# write column headings
table.cell(0, 0).text = "Cons"
table.cell(0, 1).text = "Pros"

# write body cells
table.cell(1, 0).text = "go down"
table.cell(1, 1).text = "go down together"

prs.save("table.pptx")
