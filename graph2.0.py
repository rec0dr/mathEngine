import turtle
import math

import number_stats_v as nsv
from enum import Enum

print("Welcome to my graphing calculator!")
mode = (input("Default or custom scale and center? (D/C) ") == "C")
if mode:
    scalaX = float(input("Please enter X scale: "))
    scalaY = float(input("Please enter Y scale: "))
    centerX = float(input("Please enter X center: "))
    centerY = float(input("Please enter Y center: "))
    b = int(input("Please enter window size (pixels):"))
else:
    scalaX, scalaY = 10, 10
    centerX, centerY = 0,0
    b = 500

# scalaX, scalaY, b = 25, 50, 500
eqns = []

scaleX = (280)/scalaX
scaleY = (280)/scalaY
boardSize = b
acc = 0.01
pen = turtle.Turtle()
pen.hideturtle()

pen2 = turtle.Turtle()
pen2.hideturtle()

pen3 = turtle.Turtle()
pen3.hideturtle()

turtle.title("Le, Evan - Graph Calc 1.0")

screen = turtle.Screen()
screen.setup(width=2*b,height=2*b)
pen.speed(9999)
pen2.speed(9999)
pen3.speed(9999)


def scalar_x(a):
    return (a-centerX)*boardSize/scalaX

def scalar_y(a):
    return (a-centerY)*boardSize/scalaY

def reg_x(a):
    return (a*(scalaX/boardSize)) + centerX

def reg_y(a):
    return (a*(scalaY/boardSize)) + centerY

boundD = reg_y(scalar_y(-scalaY+centerY) - 20)
boundU = reg_y(scalar_y(scalaY+centerY) + 20)
boundL = reg_x(scalar_x(-scalaX+centerX) - 20)
boundR = reg_x(scalar_x(scalaX+centerX) + 20)

# Class for enums

class TrigType(Enum):
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    CSC = "csc"
    SEC = "sec"
    COT = "cot"

class Operation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"


# Function combination logic

class Function:
    # Function combo logic
    def __init__(self, graphColor="black", graphAcc0=0.005*scalaX):
        self.graphColor = graphColor
        self.graphAcc0 = graphAcc0
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.ADD, other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.SUBTRACT, other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.MULTIPLY, other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.DIVIDE, other)
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.POWER, other)
    
    def __neg__(self):
        return Combination(Constant(0), Operation.SUBTRACT, self)
    
    # Framework for subclasses
    
    def inverse(self):
        return Parametric(self, Polynomial(1,0), tMin=-scalaX, tMax=scalaX)
    
    def evaluate(self, x):
        raise NotImplementedError
    
    def __str__(self):
        raise NotImplementedError
    
    # Graphing, tracing logic
    
    def graph(self):
        pen.pencolor(self.graphColor)
        x = boundL
        y = self.evaluate(x)
        pen.up()
        while x < boundR:
            x += self.graphAcc0
            y = self.evaluate(x)
            if y is None:
                pen.up()
                continue
            elif y > boundU or y < boundD:
                pen.up()
                continue
            else:
                pen.goto(scalar_x(x),scalar_y(y))
                pen.down()
        
        writeNewEq(self)
    
    def trace(self, x, showLines=False):
        pen3.clear()
        pen3.up()
        pen3.pencolor("red")
        y = self.evaluate(x)
        pen3.goto(scalar_x(x),scalar_y(y))
        pen3.pensize(2)
        pen3.dot()
        pen3.pensize(1)
        
        self.cursorX = x
        self.cursorY = self.evaluate(x)
        
        writeNewTrace(x,y, self)
        if showLines:
            pen3.up()
            pen3.pencolor("red")
            moveTo(self.cursorX,boundD,p3=True, up=False)
            pen3.down()
            moveTo(self.cursorX,boundU,p3=True, up=False)
            pen3.up()
            moveTo(boundL,self.cursorY,p3=True, up=False)
            pen3.down()
            moveTo(boundR,self.cursorY,p3=True, up=False)
            pen3.up()
    
    def mvtrace(self, xinc, showLines=False):
        self.trace(self.cursorX + xinc, showLines)

class Constant(Function):
    def __init__(self, value, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self.value = value
        super().__init__(graphColor, graphAcc0)
    
    def __str__(self):
        return f"y = {self.value}"
    
    def evaluate(self, x):
        return self.value

class Combination(Function):
    def __init__(self, left, operation, right, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self.left = left
        self.right = right
        self.operation = operation
        super().__init__(graphColor, graphAcc0)
    
    def evaluate(self, x):
        a = self.left.evaluate(x)
        b = self.right.evaluate(x)
        if a is None or b is None:
            return None
        
        if self.operation == Operation.ADD:
            return a + b
        elif self.operation == Operation.SUBTRACT:
            return a - b
        elif self.operation == Operation.MULTIPLY:
            return a * b
        elif self.operation == Operation.DIVIDE:
            return a / b
        elif self.operation == Operation.POWER:
            return a ** b
    
    def __str__(self):
        return f"y = ({str(self.left)[4:]}) {self.operation.value} ({str(self.right)[4:]})"
    

# Classes for eqs

class LinEq(Function):
    def __init__(self, a, b, c, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self._custom_eqString = eqString
        super().__init__(graphColor, graphAcc0)
    
    @classmethod
    def from_standard(cls, a, b, c, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        return cls(a, b, c, eqString, graphColor, graphAcc0)
    
    @classmethod
    def from_slope_intercept(cls, slope, yInt, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        return cls(-slope, 1, yInt, eqString, graphColor, graphAcc0)
    
    @classmethod
    def from_point_slope(cls, x1, y1, slope, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        return cls(-slope,1,y1 - slope*x1, eqString, graphColor, graphAcc0)
    
    @classmethod
    def from_points(cls, x1, y1, x2, y2, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        if x1 == x2:
            return cls(1, 0, x1)

        slope = (y2 - y1)/(x2 - x1)
        return cls.from_point_slope(x1, y1, slope, eqString, graphColor, graphAcc0)
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        slope = -self.a/self.b
        yInt = self.c/self.b
        
        res = "y = "
        if slope == -1:
            res = res + "-x"
        elif slope == 1:
            res = res + "x"
        elif slope != 0:
            res = res + f"{slope}x"
        
        if yInt != 0:
            if yInt < 0:
                res = res + f" - {yInt}"
            else:
                res = res + f" + {yInt}"
            
        return res
    
    def evaluate(self, x):
        return (self.c/self.b) - (self.a/self.b)*x
    
    def stats(self):
        print(f"Standard: {self.a}x + {self.b}y = {self.c}")
        print(f"eqStringing:", self.eqStringing)
    
    

class Polynomial(Function):
    
    def __init__(self, *coefficients, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self.coefficients = coefficients
        self.deg = len(self.coefficients) - 1
        self._custom_eqString = eqString
        super().__init__(graphColor, graphAcc0)
        
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            if self.deg > 1:
                eqString = "y = "
                if self.coefficients[0] == 0:
                    pass
                elif self.coefficients[0] == 1:
                    eqString = eqString + f"x^{self.deg}"
                elif self.coefficients[0] == -1:
                    eqString = eqString + f"-x^{self.deg}"
                else:
                    eqString = eqString + f"{self.coefficients[0]}x^{self.deg}"
                for i in range(1,len(self.coefficients)-2):
                    if self.coefficients[i] == 0:
                        continue
                    elif self.coefficients[i] == 1 or self.coefficients[i] == -1:
                        eqString = eqString + f"x^{self.deg - i}"
                    else:
                        eqString = eqString + f"{self.coefficients[i]}x^{self.deg - i}"
                            
                    if (self.deg - i) > 2:
                        nxt = " + " if self.coefficients[i+1] > 0 else (" - " if self.coefficients[i+1] < 0 else "")
                        eqString = eqString + nxt
        
                m = self.coefficients[len(self.coefficients)-2]
                b = self.coefficients[len(self.coefficients)-1]
                if m > 0:
                    if m == 1:
                        eqString = eqString + " + x"
                    else:
                        eqString = eqString + f" + {m}x"
                elif m < 0:
                    if m == -1:
                        eqString = eqString + " - x"
                    else:
                        eqString = eqString + f" - {-m}x"
                if b > 0:
                    eqString = eqString + f" + {b}"
                elif b < 0:
                    eqString = eqString + f" - {-b}"
                
                return eqString
            else:
                eqString = "y = "
                m = self.coefficients[0]
                b = self.coefficients[1]
                if m > 0:
                    if m == 1:
                        eqString = eqString + "x"
                    else:
                        eqString = eqString + f"{m}x"
                elif m < 0:
                    if m == -1:
                        eqString = eqString + "-x"
                    else:
                        eqString = eqString + f"{m}x"
                if b > 0:
                    eqString = eqString + f" + {b}"
                elif b < 0:
                    eqString = eqString + f" - {-b}"
                
                return eqString
                
            
    
    def evaluate(self, x):
        if len(self.coefficients) == 1:
            return self.coefficients[0]
        else:
            exp = self.deg
            res = 0
            while exp > 0:
                res += self.coefficients[self.deg-exp] * (x**exp)
                exp -= 1
            res += self.coefficients[len(self.coefficients)-1]
            return res
    
    def stats(self):
        print("Coeffs:",self.coefficients)
        print("Degree:",self.deg)
        print("Y-int:",self.coefficients[len(self.coefficients)-1]) 
        
class Exponential(Function):
    
    def __init__(self, base, vs, arg, vt, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self._data = [base, vs, arg, vt]
        self._custom_eqString = eqString
        
        self.base, self.vs, self.arg, self.vt = self._data
        super().__init__(graphColor, graphAcc0)
        
    @classmethod
    def from_basic(cls, base, vs=1, vt=0, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        return cls(base, vs, Polynomial(1,0), vt, eqString, graphColor, graphAcc0)
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        res = "y = "
        if self.vs == 0:
            return f"y = {self.vt}"
        elif self.vs == 1:
            res = res + f"({self.base})^"
        elif self.vs == -1:
            res = res + f"-({self.base})^"
        else:
            res = res + f"{self.vs}({self.base})^"
        
        res = res + f"({str(self.arg)[4:]})"
        
        if self.vt != 0:
            if self.vt > 0:
                res = res + f" + {self.vt}"
            else:
                res = res + f" - {self.vt}"
        return res
    
    def evaluate(self, x):
        return (self.vs * (self.base**self.arg.evaluate(x)) + self.vt)

class Sinusoid(Function):
    def __init__(self, vs, arg, vt, trig_type, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self.trig_type = trig_type
        self.amp, self.arg, self.vt = vs, arg, vt
        self._custom_eqString = eqString
        super().__init__(graphColor, graphAcc0)
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = "y = "
        if self.amp == -1:
            res = "-"
        elif self.amp != 1:
            res = res + f"{self.amp}*"
        
        res = res + f"{self.trig_type.value}({str(self.arg)[4:]})"
        
        if self.vt != 0:
            if self.vt < 0:
                res = res + f" - {self.vt}"
            else:
                res = res + f" + {self.vt}"
        
        return res
    
    @classmethod
    def from_basic(cls, trig_type, vs=1, vt=0, eqString=None):
        return cls(vs, Polynomial(1,0), vt, trig_type, eqString)
            
    
    def evaluate(self,x):
        theta = self.arg.evaluate(x)
        
        if self.trig_type == TrigType.SIN:
            return (self.amp * math.sin(theta)) + self.vt
        elif self.trig_type == TrigType.COS:
            return (self.amp * math.cos(theta)) + self.vt
        elif self.trig_type == TrigType.TAN:
            return (self.amp * math.tan(theta)) + self.vt
        elif self.trig_type == TrigType.CSC:
            try:
                return (self.amp * 1/(math.sin(theta))) + self.vt
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.SEC:
            try:
                return (self.amp * 1/(math.cos(theta))) + self.vt
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.COT:
            try:
                return (self.amp * 1/(math.tan(theta))) + self.vt
            except ZeroDivisionError:
                return None

class Logarithm(Function):
    def __init__(self, base, vs, arg, vt, eqString=None, graphColor = "black", graphAcc0 = 0.005*scalaX):
        self._data = [base, vs, arg, vt]
        self.base, self.vs, self.arg, self.vt = self._data
        self._custom_eqString = eqString
        super().__init__(graphColor, graphAcc0)
    
    @classmethod
    def from_basic(cls, base, vs=1, vt=0, eqString=None):
        return cls(base, vs, Polynomial(1,0), vt, eqString)
        
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = "y = "
        if self.vs == -1:
            res = "-"
        elif self.vs != 1:
            res = res + f"{self.vs}*"
        
        res = res + f"log({self.base})({str(self.arg)[4:]})"
        
        if self.vt != 0:
            if self.vt < 0:
                res = res + f" - {self.vt}"
            else:
                res = res + f" + {self.vt}"
        
        return res
        
    def evaluate(self, x):
        inpt = self.arg.evaluate(x)
        try:
            return ((self.vs * math.log(inpt, self.base)) + self.vt)
        except ValueError:
            return None
        except TypeError:
            return None

class Parametric:
    def __init__(self, argX, argY, eqString=None, tMin=-10, tMax=10):
        self._data = [argX, argY]
        self.argX, self.argY = self._data
        self._custom_eqString = eqString
        self.graphColor = "black"
        self.graphAcc0 = 0.005*scalaX
        self.tMin = tMin
        self.tMax = tMax
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            return f"P(x) = ({str(self.argX)[4:]}, {str(self.argY)[4:]})"
    
    def evaluate(self, t):
        return [self.argX.evaluate(t), self.argY.evaluate(t)]
    
    def graph(self, acc0=scalaX*0.005, color="black"):
        for eqn in eqns:
            if isinstance(eqn, Parametric):
                if self._data == eqn._data and color == eqn.graphColor and acc0 == eqn.graphAcc0 and tMin == eqn.tMin and tMax == eqn.tMax:
                    return
                elif self._data == eqn._data:
                    self.graphColor = color
                    self.graphAcc0 = acc0
                    self.tMin = tMin
                    self.tMax = tMax
                    eqns.remove(eqn)
                    eqns.append(self)
                    
                    #initial()
                    redraw()
                    return
        
        self.graphColor = color
        self.graphAcc0 = acc0
        pen.pencolor(color)
        tMin, tMax = self.tMin, self.tMax
        t = tMin
        x,y = self.evaluate(t)
        pen.up()
        while t < tMax:
            t += acc0
            x,y = self.evaluate(t)
            if y is None or x is None:
                pen.up()
                continue
            elif y > boundU or y < boundD or x < boundL or x > boundR:
                pen.up()
                continue
            else:
                pen.goto(scalar_x(x),scalar_y(y))
                pen.down()
        
        writeNewEq(self)
        
            
class Point:
    def __init__(self,x,y, eqString=None):
        self.x = x
        self.y = y
        self.graphColor = "black"
        self._data = [x,y]
        self._custom_eqString = eqString
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            return f"P = ({self.x},{self.y})"
    
    def graph(self, color="black"):
        self.graphColor = color
        pen.pencolor(self.graphColor)
        pen.up()
        pen.goto(scalar_x(self.x),scalar_y(self.y))
        pen.dot()
        writeNewEq(self)

        


#Scale change code: scalaX = []
                    #scalaY = []
                    #scaleX = 280/scalaX
                    #scaleY = 280/scalaY
                    #acc = (scalaX/10)/100
                    #clear()

# basic graphing logic

def writeNewTrace(posX, posY, obj):
    pen3.up()
    pen3.pencolor("red")
    moveTo(*botRight, p3=True)
    moveY(oneLine, p3=True)
    pen3.write(f"Equation: {str(obj)}", align="right", font=("Arial", 16, "normal"))
    moveY(-oneLine, p3=True)
    realstr = f"Current Pos: ({posX}, {posY})"
    pen3.write(realstr,  align="right", font=("Arial", 16, "normal"))
    

def writeNewEq(obj):
    global eqns
    stringeq = str(obj)
    
    pen.up()
    moveTo(*botLeft)
    moveY((len(eqns)+1)*oneLine)
    
    realstr = f"{len(eqns)+1}. " + stringeq
    pen.write(realstr,  align="left", font=("Arial", 16, "normal"))
    eqns.append(obj)

def zoom(amt):
    global scalaX, scalaY
    
    scalaX *= amt
    scalaY *= amt
    
    initial()

def zoomX(amt):
    global scalaX
    scalaX *= amt
    
    initial()

def zoomY(amt):
    global scalaY
    scalaY *= amt
    
    initial()

def setscaleX(amt):
    global scalaX
    scalaX = amt
    
    initial()

def setscaleY(amt):
    global scalaY
    scalaY = amt
    
    initial()

def setscale(amt):
    global scalaX, scalaY
    
    scalaX = amt
    scalaY = amt
    
    initial()

def setscaleXY(amtX, amtY):
    global scalaX, scalaY
    
    scalaX = amtX
    scalaY = amtY
    
    initial()

def moveCX(inc):
    global centerX
    centerX += inc
    
    initial()

def moveCY(inc):
    global centerY
    centerY += inc
    
    initial()

def moveCXY(inc, inc2):
    global centerX, centerY
    centerX += inc
    centerY += inc2
    
    initial()

def setCX(amt):
    global centerX
    centerX = amt
    
    initial()

def setCY(amt):
    global centerY
    centerY = amt
    
    initial()

def setCXY(amt, amt2):
    global centerX, centerY
    centerX = amt
    centerY = amt2
    
    initial()

def homePos():
    setCXY(0,0)

def homeScale():
    setscaleXY(10,10)

def home():
    global centerX, centerY, scalaX, scalaY
    
    scalaX = 10
    scalaY = 10
    centerX = 0
    centerY = 0
    
    initial()
    

def dot():
    pen.pensize(2)
    pen.dot()
    pen.pensize(1)


def axes():
    pen2.up()
    pen2.goto(scalar_x(boundL),scalar_y(0))
    pen2.down()
    pen2.goto(scalar_x(boundR),scalar_y(0))
    pen2.up()
    pen2.goto(scalar_x(0),scalar_y(boundD))
    pen2.down()
    pen2.goto(scalar_x(0),scalar_y(boundU))
    pen2.up()

def ruler(mx = scalaX/10, my=scalaY/10):
    pen2.up()
    index = 0
    while index < boundR:
        pen2.goto(scalar_x(index),scalar_y(scalaY/40))
        pen2.down()
        pen2.goto(scalar_x(index),scalar_y(-scalaY/40))
        pen2.up()
        print("+X",index)
        index += mx
        
    index = 0 
    while index > boundL:
        pen2.goto(scalar_x(index),scalar_y(scalaY/40))
        pen2.down()
        pen2.goto(scalar_x(index),scalar_y(-scalaY/40))
        pen2.up()
        print("-X",index)
        index -= mx
    
    pen2.goto(scalar_x(scalaX/2),scalar_y(scalaY/20))
    pen2.down()
    pen2.goto(scalar_x(scalaX/2),scalar_y(-scalaY/20))
    pen2.up()
    pen2.goto(scalar_x(scalaX/2),scalar_y(-scalaY/10))
    pen2.write(f"{(scalaX/2)}", align="center", font=("Arial", 16, "normal"))
    
    pen2.goto(scalar_x(-scalaX/2),scalar_y(scalaY/20))
    pen2.down()
    pen2.goto(scalar_x(-scalaX/2),scalar_y(-scalaY/20))
    pen2.up()
    pen2.goto(scalar_x(-scalaX/2),scalar_y(-scalaY/10))
    pen2.write(f"{-(scalaX/2)}", align="center", font=("Arial", 16, "normal"))
    
    index = 0
    while index < boundU:
        pen2.goto(scalar_x(-scalaX/40),scalar_y(index))
        pen2.down()
        pen2.goto(scalar_x(scalaX/40),scalar_y(index))
        pen2.up()
        print("+Y",index)
        index += my
        
    index = 0
    while index > boundD:
        pen2.goto(scalar_x(-scalaX/40),scalar_y(index))
        pen2.down()
        pen2.goto(scalar_x(scalaX/40),scalar_y(index))
        pen2.up()
        print("-Y",index)
        index -= my
        
    pen2.goto(scalar_x(scalaX/20),scalar_y(scalaY/2))
    pen2.down()
    pen2.goto(scalar_x(-scalaX/20),scalar_y(scalaY/2))
    pen2.up()
    pen2.goto(scalar_x(-scalaX/15),scalar_y(scalaY/2))
    pen2.write(f"{(scalaY/2)}", align="right", font=("Arial", 16, "normal"))
    
    pen2.goto(scalar_x(scalaX/20),scalar_y(-scalaY/2))
    pen2.down()
    pen2.goto(scalar_x(-scalaX/20),scalar_y(-scalaY/2))
    pen2.up()
    pen2.goto(scalar_x(-scalaX/15),scalar_y(-scalaY/2))
    pen2.write(f"{-(scalaY/2)}", align="right", font=("Arial", 16, "normal"))
    
    pen2.goto(scalar_x(0),scalar_y(0))
    pen2.pensize(2)
    pen2.dot()
    pen2.pensize(1)

def redraw():
    global eqns
    pen.clear()
    eqns2 = eqns.copy()
    eqns = []
    
    for eqn in eqns2:
        if isinstance(eqn, Parametric):
            eqn.graph(tMin=eqn.tMin, tMax=eqn.tMax, acc0=eqn.graphAcc0, color=eqn.graphColor)
        elif not isinstance(eqn, LinEq) and not isinstance(eqn, Point):
            eqn.graph(acc0=eqn.graphAcc0, color=eqn.graphColor)
        else:
            eqn.graph(color=eqn.graphColor)

def clear():
    global eqns
    pen.clear()
    eqns = []

def full_clear():
    global eqns
    pen.clear()
    pen2.clear()
    eqns = []
    
def moveTo(x,y, p2=False, p3=False, up=True):
    if p2:
        if up:
            pen2.up()
        pen2.goto(scalar_x(x),scalar_y(y))
        return
    if p3:
        if up:
            pen3.up()
        pen3.goto(scalar_x(x),scalar_y(y))
        return
    if up:
        pen.up()
    pen.goto(scalar_x(x),scalar_y(y))

def moveX(incX, p2=False, p3=False):
    x = reg_x(pen.pos()[0])
    y = reg_y(pen.pos()[1])
    if p2:
        x = reg_x(pen2.pos()[0])
        y = reg_y(pen2.pos()[1])
    if p3:
        x = reg_x(pen3.pos()[0])
        y = reg_y(pen3.pos()[1])
        
    moveTo(x+incX, y, p2, p3)

def moveY(incY, p2=False, p3=False):
    x = reg_x(pen.pos()[0])
    y = reg_y(pen.pos()[1])
    if p2:
        x = reg_x(pen2.pos()[0])
        y = reg_y(pen2.pos()[1])
    if p3:
        x = reg_x(pen3.pos()[0])
        y = reg_y(pen3.pos()[1])
        
    moveTo(x, y+incY, p2, p3)

def moveBy(incX,incY, p2=False, p3=False):
    moveX(incX, p2, p3)
    moveY(incY, p2, p3)
    
#scalaX = 5
#scalaY = 10
#scaleX = 280/scalaX
#scaleY = 280/scalaY
#acc = scalaX/1000
#clear()
        
oneLine = 0.04*scalaY

topLeft = (centerX - 0.96*scalaX, centerY + 0.93*scalaY)
topRight = (centerX + 0.96*scalaX, centerY + 0.93*scalaY)
botLeft = (centerX - 0.96*scalaX, centerY - 0.93*scalaY)
botRight = (centerX + 0.96*scalaX, centerY - 0.93*scalaY)

def initial():
    global oneLine, topLeft, topRight, botLeft, botRight, scaleX, scaleY, eqns, boundD, boundU, boundL, boundR
    
    pen.clear()
    pen2.clear()
    pen3.clear()
    
    scaleX = (280)/scalaX
    scaleY = (280)/scalaY
    
    oneLine = 0.04*scalaY

    topLeft = (centerX - 0.96*scalaX, centerY + 0.93*scalaY)
    topRight = (centerX + 0.96*scalaX, centerY + 0.93*scalaY)
    botLeft = (centerX - 0.96*scalaX, centerY - 0.93*scalaY)
    botRight = (centerX + 0.96*scalaX, centerY - 0.93*scalaY)
    
    boundD = reg_y(scalar_y(-scalaY+centerY) - 20)
    boundU = reg_y(scalar_y(scalaY+centerY) + 20)
    boundL = reg_x(scalar_x(-scalaX+centerX) - 20)
    boundR = reg_x(scalar_x(scalaX+centerX) + 20)

    axes()
    ruler(scalaX/10, scalaY/10)

    pen2.pencolor("blue")
    moveTo(*topLeft, True)
    pen2.write(f"X Scale: {scalaX}", align="left", font=("Arial", 16, "normal"))
    moveY(-oneLine, True)
    pen2.write(f"Y Scale: {scalaY}", align="left", font=("Arial", 16, "normal"))
    moveY(-oneLine, True)
    pen2.write(f"Camera Center: ({centerX}, {centerY})", align="left", font=("Arial", 16, "normal"))

    pen2.pencolor("black")
    moveTo(*botLeft, True)
    pen2.write("Equations",  align="left", font=("Arial", 16, "normal"))
    
    eqns2 = eqns.copy()
    eqns = []
    
    for eqn in eqns2:
        if isinstance(eqn, Parametric):
            eqn.graph(tMin=eqn.tMin, tMax=eqn.tMax, acc0=eqn.graphAcc0, color=eqn.graphColor)
        elif isinstance(eqn, Function):
            eqn.graph()
            


initial()
V = Polynomial(1,0)