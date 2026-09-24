from helper import *

width, height = (1000, 1000)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=90, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)
app.renderer.default_GridStyle.color = GREEN
app.renderer.default_GridStyle.minor_color = RED
app.renderer.default_GridStyle.minor_visible = False

func = (X**3) / 20
app.add_object(func, color=BLUE)
trace = TracedPoint(func, -10)
app.add_object(trace, color=RED, radius_px=5, draggable=True)
# app.add_object(Label(3, 3, text=lambda:f"{trace.parameter:.3f} -> {app.analyzer.derivative_x(func, trace.parameter):.3f}"), font_size=36)

def obj_deriv(dx1, dx2):
    dx3 = (dx1 + dx2) / 2
    m = Value(lambda: app.analyzer.derivative_x(func, trace.parameter+dx3))
    b = Value(lambda: -(app.analyzer.derivative_x(func, trace.parameter+dx3)*(trace.parameter+dx3))+(func.evaluate(trace.parameter+dx3)))
    new_func = m*X + b
    app.add_object(LineSegment((Value(lambda: trace.parameter+dx1), Value(lambda: new_func.evaluate(trace.parameter+dx1))), (Value(lambda: trace.parameter+dx2), Value(lambda: new_func.evaluate(trace.parameter+dx2)))), show_ends=False)

for i in range(5):
    obj_deriv(i-0.5, i+0.5)

app.add_animation(trace, "parameter", 5, 30, EaseType.SIN_IN_OUT)
app.run()