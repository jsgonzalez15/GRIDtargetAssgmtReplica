import numpy as np
from numpy import doc
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
import cv2

[radOper,PtOptimum,vOptimum]=GRIDFcns.CalcularParametrosEnergeticos()
print(radOper)
print(PtOptimum)
print(vOptimum)
'''
div=3
C=np.array([range((div-1)*div+1,div*div+1)]) # Matriz de indices para identificar celdas
for i in range(div-1,0,-1):
    C=np.append(C,[range((i-1)*div+1,div*i+1)],axis=0)
#print(C)

ptest=[radOper/10000,radOper/10000]
GRIDFcns.CurrentCell(ptest,C,radOper,div)

nUAVs=10
#(x,y,asign) posiciones [km] y asignaciones (+1) Lider (-1) No Asignado
initialUAVs= np.concatenate(((np.random.rand(nUAVs,2)*radOper/1000),np.zeros((nUAVs,1))),axis=1)
initialUAVs= initialUAVs[:,[0,1]]
print(initialUAVs)
#help(doc)

trying=np.array([[1,-2],[-2,3],[3,6],[-4,-2]])
tryingNorma=np.linalg.norm(trying,axis=1)
tryingNorma=np.c_[tryingNorma,tryingNorma]
print(tryingNorma)
hey=[1]
hey.append(3)
print(hey)
print(np.divide(trying,tryingNorma))
print((np.array([False, True])-1)*(-1))

a=np.c_[np.array([1,2,3]),np.array([5,7,9])]
b=np.zeros((a.shape[0],1))
print(a)
print(b)
print(np.c_[a,b])

plt.scatter([1,2,3,4],[1,2,3,3],marker='o',c='None', edgecolor='red',lineWidth=0.7,label='Objetivos')
plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.title('Evolución de envios distribuidos')
plt.legend()

plt.gcf().canvas.draw()
img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
# display image with opencv or any operation you like
cv2.imshow("plot",img)
cv2.waitKey()
a=np.array([True, True])
print(a.all()==True)'''
a=np.array([[1,1],[2,3],[4,5],[6,7],[5,5],[6,9],[17,10],[8,90]])
print(a[0:0])
a=np.delete(a,[0,1,4],0)
print(a)
a[2:5,1]=1
print(a[:,0:2])

matriz=[[1,2,3,4,5,6],[2,-1,-4,-5,3,6],[6,5,4,3,2,1]]
n=[(y,i,matriz[y][i]) for y in range(len(matriz)) for i in range(len(matriz[0])) if  matriz[y][i]>0]
print(n)
