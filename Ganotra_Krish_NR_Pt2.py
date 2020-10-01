'''
Krish Ganotra
Newton Raphson Part 2
'''
import math

def extremaMulti(x, y, f, f01, f10, f11, f20, f02):
    dx,dy = 1,1
    while(dx**2+dy**2 >= 0.0000000000001):
        H = [[f20(x,y), f11(x,y)],
            [f11(x,y), f02(x,y)]]
        Hinv = inverse(H)

        grad = [[f10(x,y)],
                [f01(x,y)]]

        dx,dy = [i[0] for i  in matmult(Hinv,grad)]
        x -= dx*0.1
        y -= dy*0.1

    # v_n+1 = v_n - H^(-1)(grad(f_v_n))
    return x,y,f(x,y)

def zeroMulti(x, y, f1, f2, f1_10, f1_01, f2_10, f2_01):
    dx, dy = 1,1
    while(dx**2+dy**2 >= 0.0000000000001):
        J = [[f1_10(x,y), f1_01(x,y)],
            [f2_10(x,y), f2_01(x,y)]]
        Jinv = inverse(J)

        fa = [[f1(x,y)],
            [f2(x,y)]]

        dx,dy = [i[0] for i in matmult(Jinv, fa)]
        x-=dx*0.1
        y-=dy*0.1
    # print(f1(x,y), f2(x,y))
    return x,y


def inverse(mat):
    if(len(mat)==2 and len(mat[0])==2):
        x,y = mat
        a,b = x
        c,d = y
        a,b,c,d = [x/(a*d-b*c) for x in [a,b,c,d]]
        return [[d,-b],[-c,a]]

def matmult(mat1, mat2):
    newMat = []
    for r1 in range(len(mat1)):
        row = []
        for c2 in range(len(mat2[0])):
            cell = sum(mat1[r1][i]*mat2[i][c2] for i in range(len(mat1[r1])))
            row.append(cell)
        newMat.append(row)
    return newMat

extremaFuncs = [(lambda x,y: (x-2)**2 + y**2 - 3, lambda x,y: 2*y, lambda x,y: 2*x-4, lambda x,y: 0, lambda x,y: 2, lambda x,y: 2),
                (lambda x,y: x**(4/3) + y**(4/3), lambda x,y: 4/3*y**(1/3), lambda x,y: 4/3*x**(1/3), lambda x,y: 0, lambda x,y: 4/9*x**(-2/3), lambda x,y: 4/9*x**(-2/3)),
                (lambda x,y: (x-2)*2 + (y-3)**2 + 7, lambda x,y: 2*y-6, lambda x,y: 2*x-4, lambda x,y: 0, lambda x,y: 2, lambda x,y: 2),
                (lambda x,y: y*x**2 + 3*x*y**2 + 8*x*y + 4*y + 9, lambda x,y: x**2 + 6*x*y + 8*x + 4, lambda x,y: 2*y*x + 3*y**2 + 8*y, lambda x,y: 2*x + 6*y + 8, lambda x,y: 2*y, lambda x,y: 6*x),
                (lambda x,y: math.exp(x*y)+(x-3)**2+(y-7)**2, lambda x,y: x*math.exp(x*y)+2*(y-7), lambda x,y: y*math.exp(x*y)+2*(x-3), lambda x,y: y*x*math.exp(x*y)+math.exp(x*y), lambda x,y: y**2*math.exp(x*y)+2, lambda x,y: x**2*math.exp(x*y)+2),
                ]

f, f01, f10, f11, f20, f02  = extremaFuncs[-1]
x0,y0 = 1,1
print("The local minimum is at: (%.6f, %.6f, %.6f)" % extremaMulti(x0,y0, f, f01, f10, f11, f20, f02))


zeroFuncs = [(lambda x,y: x**2+x*y-4, lambda x,y: y**2+x*y-1, lambda x,y: 6*x+y, lambda x,y: x, lambda x,y: y, lambda x,y: 2*y+x),
            (lambda x,y: 3*x-5*y+13, lambda x,y: y - 4*x + 7, lambda x,y: 3, lambda x,y: -5, lambda x,y: -4, lambda x,y: 1),
            (lambda x,y: math.exp(x)+math.exp(y)-x**2-y**2, lambda x,y: math.sin(x+2*y), lambda x,y: math.exp(x)-2*x, lambda x,y: math.exp(y)-2*y, lambda x,y: math.cos(x+2*y), lambda x,y: 2*math.cos(x+2*y)),
            ]

f1, f2, f1_10, f1_01, f2_10, f2_01 = zeroFuncs[-1]
x0,y0 = 0,0
print("The value of the zero is : (%.6f, %.6f)" % zeroMulti(x0, y0, f1, f2, f1_10, f1_01, f2_10, f2_01))
