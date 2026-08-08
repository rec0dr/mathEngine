from .function import Function, Value

class Polynomial(Function):
    
    def __init__(self, *coefficients, eqString=None):
        super().__init__()
        self.coefficients = list(coefficients)
        for i in range(len(self.coefficients)):
            if isinstance(self.coefficients[i], (int, float)):
                self.coefficients[i] = Value(self.coefficients[i])
        self.deg = len(self.coefficients) - 1
        self._custom_eqString = eqString

    def derivative(self):
        coeffs = []
        for i in range(len(self.coefficients)-1):
            coeffs.append((len(self.coefficients)-1-i) * self.coefficients[i].evaluate(0))
        return Polynomial(*coeffs, eqString=self._custom_eqString)

    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            string = ""
            for i in range(len(self.coefficients)):
                if self.coefficients[i] != 0:
                    string += f"{str(self.coefficients[i])}x^{self.deg - i}"

                if i < len(self.coefficients)-1:
                    if self.coefficients[i+1].evaluate(0) > 0:
                        string += " + "
                    elif self.coefficients[i+1].evaluate(0) < 0:
                        string += " - "
                    

            return string
                
            
    
    def evaluate(self, x):
        if len(self.coefficients) == 1:
            return self.coefficients[0].evaluate(x)
        else:
            exp = self.deg
            res = 0
            while exp > 0:
                res += self.coefficients[self.deg-exp].evaluate(x) * (x**exp)
                exp -= 1
            res += self.coefficients[len(self.coefficients)-1].evaluate(x)
            return res
    
    def stats(self):
        print("Coefficients:",self.coefficients)
        print("Degree:",self.deg)
        print("Y-int:",self.coefficients[len(self.coefficients)-1]) 