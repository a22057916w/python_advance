import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches

from pptx.dml.color import RGBColor

prs = Presentation()
title_only_slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(title_only_slide_layout)
shapes = slide.shapes

shapes.title.text = "Adding a Table"

rows = cols = 2
left = top = Inches(0)
width = Inches(2)
height = Inches(3)


table = shapes.add_table(rows, cols, left, top, width, height).table

table.columns[0].width = Inches(2)
table.columns[1].width = Inches(2)

# write column headings
table.cell(0, 0).text = "Cons"
table.cell(0, 1).text = "Pros"

# write body cells
table.cell(1, 0).text = "go down"
table.cell(1, 1).text = "go down together\n1234567981231dsa5fasdf4saf5as4dfas4d5f456sd4fsa64\n165sad4f65sad4fasd54f"
p = table.cell(1,1).text_frame.paragraphs[0]
run = p.add_run()
run.text = "FFFFFFFF"
font = run.font
print(font.keys())
font.color.rgb = RGBColor(255, 0, 0)
print(table.cell(1,1).text_frame.paragraphs[0].text)
print(len(table.cell(1,1).text_frame.paragraphs[0].runs))
prs.save("./result/table.pptx")
