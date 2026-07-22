from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_AxisStyle.arrow_dims = (20,10)

func0 = SIN
func1 = TAN

animConst = LineSegment((3,3), (5,-5))
app.add_animations(Animation(animConst, "pos1", (1, -3), 5, EaseType.SIN_IN_OUT), Animation(animConst, "pos2", (7, 5), 5, EaseType.SIN_IN_OUT))
app.add_object(animConst, color=BLUE, label_ends=True)
app.run()