from helper import *

width, height = (1000, 1000)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=500, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)
app.renderer.default_GridStyle.color = GREEN
app.renderer.default_GridStyle.minor_color = RED
app.renderer.default_GridStyle.minor_visible = True

a = Point(0,0)
app.add_object(a, color=BLUE, radius_px=5, draggable=True)
r = 1
tps = []
def add_planet():
    global r, tps
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    circle = PARAMETRIC_CIRCLE(r, (Value(lambda: a.x), Value(lambda: a.y)))
    app.add_object(circle, show_ui=False, color=color)
    tps.append(TracedPoint(circle,0))
    app.add_object(tps[-1], show_ui=True, show_type=False, name=f"Planet {len(tps)-1}", color=color, radius_px=5)
    app.add_animation(tps[-1], "parameter", 2*PI, random.random()*20, two_way=False)
    r += 1

def switch_minor():
    app.renderer.default_GridStyle.minor_visible = not app.renderer.default_GridStyle.minor_visible

def set_move_speed():
    speed = float(input("New move speed: "))
    app.camera_controller.speed = speed

def double_move_speed():
    app.camera_controller.speed *= 2

def half_move_speed():
    app.camera_controller.speed *= 0.5

app.key_binds = {pygame.K_0: add_planet, pygame.K_1: switch_minor, pygame.K_2: set_move_speed, pygame.K_3: double_move_speed, pygame.K_4: half_move_speed}
app.run()