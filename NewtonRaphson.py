import math

def zero(x, f, f1):
    while abs(dx:=f(x)/f1(x)) >= 0.00001:
        x -= dx
    return x

def min(x, f, f1, f2):
    while abs(dx:=f1(x)/f2(x)) >= 0.00001:
        x -= dx
    return x

x0 = 2
functions = [
(lambda x: x**(4/3), lambda x: 4/3*(x**(1/3)), lambda x: 4/9*(x**(-2/3))),
(lambda x: x**4 + x**3 - x**2, lambda x: 4*x**3 + 3*x**2 - 2*x,  lambda x:12*x**2 + 6*x - 2),
(lambda x: x**2 - x - 1, lambda x: 2*x -1,  lambda x:2),
(lambda x: math.exp(x) - 4*math.sin(x), lambda x: math.exp(x)-4*math.cos(x),  lambda x:math.exp(x)+4*math.sin(x)),
(lambda x: x**3-5*x**2+4*x, lambda x: 3*x**2-10*x+4,  lambda x:2),
]


f,f1,f2 = functions[1]
print("The value of the zero is : ", "%.4f"% zero(x0, f, f1))
print("The local minimum is at: ", "%.4f"% min(x0, f, f1, f2))

'''
a. If the tangent drawn from the point on the curve never meets the X axis (that is, the tangent becomes parallel to X axis)

d. The derivatives tends to zero. See that there is a f’(Xn) term in the RHS of the Newton raphson equation. If this tends to 0, then the value of RHS tends to infinity (As anything divided by 0 is infinity).

e. The initial guess made for the root is so bad.
'''
