import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation


prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Fuck Off"
subtitle.text = "Will You?"

prs.slides.add_slide(title_slide_layout)
print(len(prs.slides))

# for shape in slide.shapes:
#     if shape.is_placeholder:
#         phf = shape.placeholder_format
#         print('%d, %s' % (phf.idx, phf.type))

prs.save("./result/Presentation.pptx")
