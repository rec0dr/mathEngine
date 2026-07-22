from .function import Function

class Polynomial(Function):
    
    def __init__(self, *coefficients, eqString=None):
        super().__init__()
        self.coefficients = coefficients
        self.deg = len(self.coefficients) - 1
        self._custom_eqString = eqString
        
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            if self.deg > 1:
                eqString = ""
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
                eqString = ""
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
        print("Coefficients:",self.coefficients)
        print("Degree:",self.deg)
        print("Y-int:",self.coefficients[len(self.coefficients)-1]) 