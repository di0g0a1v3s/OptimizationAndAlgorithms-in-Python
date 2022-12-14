# -*- coding: utf-8 -*-
"""OA_Parte3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16eVxtehFcTd01iqGThatyTQnGkK19L7R
"""

# Import packages.
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

#--------TASK 1-------------
# Import data
dataset = np.genfromtxt("data_opt.csv", delimiter=',')
N=dataset.shape[0]
print("N =",N)
D = np.zeros([N, N])

for m in range(N):
    for n in range(N):
        D[m,n] = np.linalg.norm(dataset[m]-dataset[n])


print("D[2][3] =", D[2-1,3-1])
print("D[4][5] =", D[4-1,5-1])

max = 0
maximizer = np.array([0, 0])

for m in range(N):
    for n in range(N):
        if D[m,n] > max:
            max = D[m,n]
            maximizer = np.array([m, n])

print("Maximum distance =",max,", Maximizer pair of points =",maximizer+np.array([1, 1]))

#--------TASK 2-----------
def MatrixToArray(M):   # (200,2) -> (400,1)
    return np.reshape(M,(M.shape[0]*M.shape[1],1))
    
def f(y):
    sum = 0
    for m in range(N):
        for n in range(m+1,N):
            sum = sum + (f_nm(n,m,y))**2
    return sum

def f_nm(n,m,y):
    return (np.linalg.norm(y[m]-y[n]) - D[m,n])

def f_nm_derivative(n,m,y):
    ret = np.zeros([N,y.shape[1]])
    ret[m] = (y[m]-y[n])/np.linalg.norm(y[m]-y[n])
    ret[n] = (y[n]-y[m])/np.linalg.norm(y[m]-y[n])
    return ret

def f_derivative(y):
    ret = np.zeros([N,y.shape[1]])
    for m in range(N):
        for n in range(m+1,N):
            ret = ret + 2*f_nm(n,m,y)*f_nm_derivative(n,m,y)
    return ret


def A(y, lam):
    p=0
    K = y.shape[1]
    ret = np.zeros([int((N**2-N)/2) , N*K])

    for m in range(N):
        for n in range(m+1,N):
            aux = np.transpose(MatrixToArray(f_nm_derivative(n,m,y)))
            ret[p] = aux
            p=p+1
    ret = np.vstack((ret, np.sqrt(lam)*np.identity(N*K)))
    return ret

def b(y, lam):
    p=0
    ret = np.zeros([int((N**2-N)/2),1])

    for m in range(N):
        for n in range(m+1,N):
            aux = np.transpose(MatrixToArray(f_nm_derivative(n,m,y))).dot(MatrixToArray(y)) - f_nm(n,m,y)
            ret[p] = aux
            p=p+1

    ret = np.vstack((ret, np.sqrt(lam)*MatrixToArray(y)))
    return ret

#--------TASK 3-------------


def LM(lambda_0, epsilon, k, y_init):
    lambda_i = lambda_0

    y_i = y_init.reshape(N, k)

    fig = plt.figure()
    if k ==2:
        plt.plot(y_i[:,0], y_i[:,1], 'bo')
    elif k==3:
        ax = Axes3D(fig)
        ax.scatter(y_i[:,0], y_i[:,1],y_i[:,2], 'bo')


    i=0
    
    cost = []
    gradient_norm = []
    while True:
        g_i = f_derivative(y_i)
        print("Iteration",i,", Gradient Norm =",np.linalg.norm(g_i),", Cost Function =", f(y_i))
        if np.linalg.norm(g_i) < epsilon:
            break
        
        A_i = A(y_i, lambda_i)
        b_i = b(y_i, lambda_i)
        y_hat,_,_,_ = np.linalg.lstsq(A_i,b_i,rcond=None) #np.linalg.inv(np.transpose(A_i).dot(A_i)).dot(np.transpose(A_i)).dot(b_i)
        y_hat = y_hat.reshape(N, k)
        if f(y_hat) < f(y_i):
            y_i = y_hat
            lambda_i = 0.7*lambda_i
        else:
            lambda_i = 2*lambda_i 
        i=i+1
        cost = np.append(cost, f(y_i))
        gradient_norm = np.append(gradient_norm, np.linalg.norm(f_derivative(y_i)))
   
    fig = plt.figure()
    if k==2:
        plt.plot(y_i[:,0], y_i[:,1], 'bo')
    
    else:
        ax = Axes3D(fig)
        ax.scatter(y_i[:,0], y_i[:,1],y_i[:,2], 'bo')
    plt.grid()
    plt.figure()
    plt.plot(range(cost.shape[0]), cost, label='Cost')
    plt.yscale("log")
    plt.grid()
    plt.legend()
    plt.figure()
    plt.plot(range(gradient_norm.shape[0]), gradient_norm, label = 'Gradient Norm')
    plt.grid()
    plt.yscale("log")
    plt.legend()
    
    


y_init = np.genfromtxt('yinit2.csv', delimiter=',')
LM(1, 10**-2 * 2, 2, y_init)
plt.show()
y_init = np.genfromtxt('yinit3.csv', delimiter=',')
LM(1, 10**-2 * 3, 3, y_init)
plt.show()

#------------TASK 4--------------------
dataset = np.genfromtxt("dataProj.csv", delimiter=',')
N=dataset.shape[0]
print("N =",N)
D = np.zeros([N, N])

for m in range(N):
    for n in range(N):
        D[m,n] = np.linalg.norm(dataset[m]-dataset[n])

k=2
lambda_0 = 1
epsilon = k*10**(-4)

y_init = np.array(range(N*k))
LM(lambda_0, epsilon, k, y_init)
plt.show()


y_init = -np.array(range(N*k))
LM(lambda_0, epsilon, k, y_init)
plt.show()

y_init = np.random.rand(N*k)*200
LM(lambda_0, epsilon, k, y_init)
plt.show()