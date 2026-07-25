from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_AxisStyle.arrow_dims = (20,10)

# CUSTOM CODE IS BEYOND THIS POINT

def constructAnimatedPoint(x1, y1, x2, y2, point_style: PointStyle = PointStyle(color=(255,0,0), radius_px = 7, labeled=True), line_segment_style: LineSegmentStyle = LineSegmentStyle(color=(0,0,255), opacity=128, thickness=4, show_ends=True, label_ends=True), duration=2, loop=True, two_way=True, ease_type=EaseType.SIN_IN_OUT):
    point = Point((x1, y1))
    anim1 = Animation(point, "pos", (x2, y2), duration, ease_type, None, loop, two_way)
    app.add_animations(anim1)
    app.add_graph_objects(GraphObject(LineSegment((x1, y1), (x2, y2)), line_segment_style))
    app.add_object(Parametric(COS + Value(lambda: point.x), SIN + Value(lambda: point.x), -100, 100))
    app.add_graph_objects(GraphObject(point, point_style))


    app.add_object(
        LineSegment(
            [
                dynamic(lambda: point.x),
                dynamic(lambda: point.y)
            ],
            [
                dynamic(lambda: point.x) + dynamic(lambda: math.cos(2*PI*min(anim1.elapsed / anim1.duration, 1))),
                dynamic(lambda: point.y) + dynamic(lambda: math.sin(2*PI*min(anim1.elapsed / anim1.duration, 1)))
            ]
        )
    )
    

constructAnimatedPoint(2,2,5,5, point_style = PointStyle(radius_px = 10, labeled=True), duration=10, ease_type=EaseType.CUBIC_IN_OUT)
app.run()