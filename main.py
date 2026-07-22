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

animPoint = TracedPoint(SIN, 2)
app.add_objects((SIN, {"color": RED, "show_arrows": True}), (TAN, {"color": BLUE, "show_arrows": True}))
app.run()