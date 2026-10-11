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

theta = Point(0,0)
x = Value(lambda: theta.x)
app.add_object(theta, draggable=True, lock_type=LockType.Y, color=BLUE, radius_px=8)
app.add_object(Polar(5*SIN(x*X), 0, 2*PI))
app.run()