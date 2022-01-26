import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt

img_path = "./.meta/amelia.jpg"

prs = Presentation()
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = Inches(1)
pic = slide.shapes.add_picture(img_path, left, top)

left = Inches(5)
width = Inches(16)
height = Inches(10)

pic = slide.shapes.add_picture(img_path, left, top, width=width, height=height)

prs.save("./result/picture.pptx")
