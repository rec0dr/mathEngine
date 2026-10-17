from helper import *

width, height = (1000, 1000)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=500, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)
app.renderer.default_GridStyle.color = GREEN
app.renderer.default_GridStyle.minor_color = RED
app.renderer.default_GridStyle.minor_visible = True

tps = []

def switch_minor():
    app.renderer.default_GridStyle.minor_visible = not app.renderer.default_GridStyle.minor_visible

def set_move_speed():
    speed = float(input("New move speed: "))
    app.camera_controller.speed = speed

def double_move_speed():
    app.camera_controller.speed *= 2

def half_move_speed():
    app.camera_controller.speed *= 0.5

app.key_binds = {pygame.K_1: switch_minor, 
                 pygame.K_2: set_move_speed, 
                 pygame.K_3: double_move_speed, 
                 pygame.K_4: half_move_speed}

p1 = Point(1,2)
p2 = Point(5,3)
sum = Value(lambda: p1.x) * Value(lambda: p2.x)
p3 = Point(Value(lambda: p1.x) * Value(lambda: p2.x), Value(lambda: p1.y) * Value(lambda: p2.y))

print(type(Value(lambda: p1.x) * Value(lambda: p2.x)))

app.add_object(p1, radius_px=8, draggable=True)
app.add_object(p2, radius_px=8, draggable=True)
app.add_object(p3, radius_px=10, color=GREEN)
app.add_object(LineSegment(p1,p2))
app.add_object(LineSegment(p2,p3))
app.add_object(LineSegment(p3,p1))

app.run()