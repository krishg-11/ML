'''
Krish Ganotra
Newton Raphson Part 1
'''
import math

def zero(x, f, f1):
    while abs(dx:=f(x)/f1(x)) >= 0.0000001:
        x -= dx*0.1
    return x,f(x)

def extrema(x, f, f1, f2):
    while abs(dx:=f1(x)/f2(x)) >= 0.0000001:
        x -= dx*0.1
    return x,f(x)

x0 = 1
functions = [
(lambda x: x**(4/3), lambda x: 4/3*(x**(1/3)), lambda x: 4/9*(x**(-2/3))),
(lambda x: x**(1/3), lambda x: 1/3*(x**(-2/3)), lambda x: -2/9*(x**(-5/3))),
(lambda x: x**(1/5), lambda x: 1/5*(x**(-4/5)), lambda x: -4/25*(x**(-9/5))),
(lambda x: x**4 + x**3 - x**2, lambda x: 4*x**3 + 3*x**2 - 2*x,  lambda x:12*x**2 + 6*x - 2),
(lambda x: x**2 - x - 1, lambda x: 2*x -1,  lambda x:2),
(lambda x: math.exp(x) - 4*math.sin(x), lambda x: math.exp(x)-4*math.cos(x),  lambda x:math.exp(x)+4*math.sin(x)),
(lambda x: x**3-5*x**2+4*x, lambda x: 3*x**2-10*x+4,  lambda x:2),
(lambda x: 2*x+7, lambda x: 2,  lambda x:0),
(lambda x: x**2-3*x-7, lambda x: 2*x-3,  lambda x:2),
(lambda x: x+math.exp(math.sin(x))+7, lambda x: 1+math.cos(x)*math.exp(math.sin(x)),  lambda x:(math.cos(x))**2*math.exp(math.sin(x))-math.sin(x)*math.exp(math.sin(x))),
(lambda x: math.sin(x)-2*math.cos(3*x)+x/2, lambda x: math.cos(x)+6*math.sin(3*x)+1/2,  lambda x:-math.sin(x)+18*math.cos(3*x)),
(lambda x: (10+7+4*x)**(1/2)-5*x/6, lambda x: 2*(10+7+4*x)**(-1/2)-5/6,  lambda x:-4*(10+7+4*x)**(-3/2)),
]


f,f1,f2 = functions[-1]
print("The value of the zero is: (%.6f, %.6f)" % zero(x0, f, f1))
print(f"The local minimum is at: (%.6f, %.6f)" % extrema(x0, f, f1, f2))
