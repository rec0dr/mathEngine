import math

from functions.__init__ import *

class Analyzer:

    def intersection(self, f: Curve, g: Curve, boundL=-10, boundR=10, iter=10, precision=10**-5):
        # Upper bounds
        if iter > 14:
            iter = 14

        if precision < 10**-15:
            precision = 10**-15

        acc = (boundR - boundL)
        curIter = 0

        while curIter < iter:

            minVal = None
            minX = None
            acc /= 10
            x = boundL

            while x < boundR:
                if f.evaluate(x) is None or g.evaluate(x) is None:
                    x += acc
                    continue
                val = abs(f.evaluate(x) - g.evaluate(x))
                
                if minVal is None:
                    minVal = val
                    minX = x
                    
                elif val < minVal:
                    minVal = val
                    minX = x

                x += acc

            if (minX - acc) > boundL:
                boundL = minX - acc

            if (minX + acc) < boundR:
                boundR = minX + acc

            curIter += 1

            #print(curIter, minVal, minX, boundL, boundR)

        if minVal > precision:
            raise ValueError("No intersections found in given range! Smallest error: " + str(minVal) + " @ x = " + str(minX))
        
        print(f"Intersection: ({minX:g}, {f.evaluate(minX):g})")
        print(f"Error: {minVal}")

        return minX, f.evaluate(minX)

    def zero(self, f: Function, boundL=-10, boundR=10, iter=10, precision=10**-5):
        # Upper bounds
        if iter > 17:
            iter = 17

        if precision < 10**-15:
            precision = 10**-15

        acc = (boundR - boundL)
        curIter = 0

        while curIter < iter:

            minVal = None
            minX = None
            acc /= 10
            x = boundL

            while x < boundR:
                val = abs(f.evaluate(x))
                if minVal is None:
                    minVal = val
                    minX = x
                    
                elif val < minVal:
                    minVal = val
                    minX = x

                x += acc

            if (minX - acc) > boundL:
                boundL = minX - acc

            if (minX + acc) < boundR:
                boundR = minX + acc

            curIter += 1

            #print(curIter, minVal, minX, boundL, boundR)

        if minVal > precision:
            raise ValueError("No zeros found in given range! Closest value: " + str(minVal) + " @ x = " + str(minX))
        
        print(f"Zero: {minX:g}")
        print(f"Error: {minVal}")

        return minX, f.evaluate(minX)

    def derivative(self, f: Curve):
        return f.derivative()

    def derivative_x(self, f: Function, x: float, acc: float = 0.000001):
        x1 = x - acc
        y1 = f.evaluate(x1)
        x2 = x + acc
        y2 = f.evaluate(x2)

        return (y2 - y1) / (x2 - x1)

