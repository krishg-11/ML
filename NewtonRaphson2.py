def extrema(x, y, f, f01, f10, f11, f20, f02):
    dx,dy = 1,1
    while(abs(dx) >= 0.00001 and abs(dy)>= 0.00001):
        H = [[f20(x,y), f11(x,y)],
            [f11(x,y), f02(x,y)]]
        Hinv = inverse(H)

        grad = [[f10(x,y)],
                [f01(x,y)]]

        dx,dy = [i[0] for i  in matmult(Hinv,grad)]
        x -= dx
        y -= dy

    # v_n+1 = v_n - H^(-1)(grad(f_v_n))
    return x,y

def zero(x, y, f1, f2, f1_10, f1_01, f2_10, f2_01):
    dx, dy = 1,1
    while(abs(dx) >= 0.00001 and abs(dy)>= 0.00001):
        J = [[f1_10(x,y), f1_01(x,y)],
            [f2_10(x,y), f2_01(x,y)]]
        Jinv = inverse(J)

        fa = [[f1(x,y)],
            [f2(x,y)]]

        dx,dy = [i[0] for i in matmult(Jinv, fa)]
        x-=dx
        y-=dy

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

extremaFuncs = [(lambda x,y: (x-2)**2 + y**2 - 3, lambda x,y: 2*y, lambda x,y: 2*x-4, lambda x,y: 0, lambda x,y: 2, lambda x,y: 2)]

zeroFuncs = [(lambda x,y: x**2+x*y-4, lambda x,y: y**2+x*y-1, lambda x,y: 6*x+y, lambda x,y: x, lambda x,y: y, lambda x,y: 2*y+x)]

f, f01, f10, f11, f20, f02  = extremaFuncs[0]
x0,y0 = 1,1
print(extrema(x0,y0, f, f01, f10, f11, f20, f02))

f1, f2, f1_10, f1_01, f2_10, f2_01 = zeroFuncs[0]
x0,y0 = 1,1
print(zero(x0, y0, f1, f2, f1_10, f1_01, f2_10, f2_01))
