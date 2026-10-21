from helper import *

width, height = (720, 720)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=500, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)

# Example 1: Changing Default Colors / Styles
# app.renderer.default_xxxx = xxx
app.renderer.default_GridStyle.color = GREEN
app.renderer.default_GridStyle.minor_color = RED
app.renderer.default_GridStyle.minor_opacity = 170
app.renderer.default_GridStyle.minor_visible = True

# Example 2: Adding Custom Keybinds
# a) Define all your functions | 1 for each key
def switch_minor():
    app.renderer.default_GridStyle.minor_visible = not app.renderer.default_GridStyle.minor_visible

def double_move_speed():
    app.camera_controller.speed *= 2

def half_move_speed():
    app.camera_controller.speed *= 0.5

# b) Define how each key links up to a function
# app.key_binds = {KEY_NAME: FUNCTION_NAME}
app.key_binds = {pygame.K_1: switch_minor,  
                 pygame.K_2: double_move_speed, 
                 pygame.K_3: half_move_speed}

# Example 3: Creating a Function
# Simply define a variable as that function of X
func1 = X**2
func2 = X*LN(X) + 15
func3 = Parametric(SIN(X), COS(X), tMin=0, tMax=2*PI)

# Example 4: Creating an Object
# Simply define a variable as that object
obj1 = Point(8,8)
obj2 = LineSegment(obj1, (5,5))
obj3 = Circle((10,10), 5)

# Example 5: Adding the Objects
# Use app.add_object() as the simplest method for adding any object to the app for drawing

# You can also style the objects within the method as parameters; 
# check the documentation/files to find all the style attributes of each object
app.add_object(func1, name="Simple Parabola", show_type=False)
app.add_object(func2, color=BLUE, name="Logarithm", show_type=False)
app.add_object(func3, visible=False, name="Parametric Circle", show_type=False)

app.add_object(obj1, draggable=True, radius_px=8, color=GREEN)
app.add_object(obj2)
app.add_object(obj3, color=GREEN, name="Circle", show_type=False)

# This runs the app - You should never have to delete this!!
app.run()