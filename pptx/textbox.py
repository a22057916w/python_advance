import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = width = height = Inches(1)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame

tf.text = "Fuck this shit (tf.text)"

p = tf.add_paragraph()
p.text = "Bold text for fuck's sake"
p.font.bold = True

p = tf.add_paragraph()
p.text = "Size-40 for fuck's sake"
p.font.size = Pt(40)

prs.save("./result/textbox.pptx")
