from helper import *

width, height = (1000, 1000)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=90, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)
app.renderer.default_GridStyle.color = GREEN
app.renderer.default_GridStyle.minor_color = RED
app.renderer.default_GridStyle.minor_visible = True

a = Point(0,5)
b = Point(5,0)
app.add_object(PARAMETRIC_ELLIPSE(Value(lambda: b.x), Value(lambda: a.y), (0,0)))
app.add_object(a, color=GREEN, radius_px=5, draggable=True, lock_type=LockType.X)
app.add_object(b, color=BLUE, radius_px=5, draggable=True, lock_type=LockType.Y)
app.run()