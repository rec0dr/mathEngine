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

val = Value(0)
animConst = Sinusoid(1, X-val, 0, TrigType.SIN)
app.add_animations(Animation(val, "value", 1, 5, EaseType.SIN_IN_OUT))
app.add_object(animConst, color=BLUE)
app.run()