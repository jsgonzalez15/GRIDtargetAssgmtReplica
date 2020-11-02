"""
2. Réplica método distribuido GRID target Assignment y extensión a asignación de tareas no monotónicas.

Temas:
* Consumo energético.
* Eficiencia de método iterativo.
* Incidencia en concentración de agentes y división iterativa.
* Efectos de puntos de inicio en el mapa.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import cv2
######################################################################################################
##                          Simulación Metodos Distribuidos: GRID Assignment
######################################################################################################

#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum]=GRIDFcns.CalcularParametrosEnergeticos()

[densidadMin,densidadMax]=[15,15] #Rango de densidades a simular
consumoDensidad=[] #valores medios y desviación estándar por densidad
consumoIteracion=[] #valores medios y desviación estándar en consumo por iteración
desviacionConsumoUAVs=0 #max desv de consumo entre UAVs (ideal 0)
divIniciales=3 #divisiones iniciales
placesPerUAV=10
dt=0.3

video=0 #obtener un video de simulación (1) ejecutar sin video (0)
autom=1 #autom sim(1)/ver todo(0)
changeDiv=1 #cambiar div durante sim(1)/ mantener div(0)
simulacionesPorDensidad=100 #n sim por densidad
video=True #guardar video de la simulación
firstAsign=True

######################################################################################################
##                          Simulacion para diferentes densidades por celda
######################################################################################################
for densidadActualSim in range(densidadMin,densidadMax+1,2): #Densidad (#targets/celda)

    consumoTotal=[] #Vector de Consumo en toda la sim
    consumoAcumulado=[]  #Vector de Consumo acumulado por sim 
    ''' ############################  Inicializacion escenario, UAVs y objetivos  ############################ '''
    actualizaciones=0
    if autom:
        div=divIniciales #div default
    else:
        div=input('Ingrese el numero de divisiones') #base y altura de la malla (div personalizado)

    nPlaces=densidadActualSim*div**2
    nUAVs=round(nPlaces/placesPerUAV) #Numero de UAVs segun densidad deseada
    places=np.random.rand(nPlaces,2)*radOper/1000 #(x,y) posiciones [km] en AreaOperaciones 
    consumoUAVs= np.zeros(nUAVs) #Registro de consumo por UAV

    #(x,y,asign) posiciones [km] y asignaciones (+1) Lider (-1) No Asignado
    initialUAVs= np.concatenate(((np.random.rand(nUAVs,2)*radOper/1000),np.zeros((nUAVs,1))),axis=1)

    if firstAsign:
        initialUAVsZero=initialUAVs #ubicaciones iniciales para ploteo de trayectorias
        firstAsign=False

    initialUAVsZero=initialUAVs #ubicaciones iniciales para ploteo de trayectorias
    C=np.array([range((div-1)*div+1,div*div+1)]) # Matriz de indices para identificar celdas
    for i in range(div-1,0,-1):
        C=np.append(C,[range((i-1)*div+1,div*i+1)],axis=0)
    
    GRIDFcns.initialScatter(places,initialUAVs,initialUAVsZero,div,radOper,C,autom,video) #Estado inicial de algoritmo
    deltaMatrix=np.zeros([div*2,div])
    deltaRight=np.zeros(div) #Matriz de deltas a actualizar por lideres en celdas
    
    ####################################################################################################################################################
    ##  (INICIO)                             Simulacion de asignacion Monotonica GRID target Assgmt (Densidad Actual)
    ####################################################################################################################################################
    placesMet=np.array([]) #Objetivos que han sido alcanzados
    iterations=0 #Iteraciones hasta alcanzar objetivos
    if video:
        fourcc=cv2.VideoWriter_fourcc(*'XVID')
        theVideo=cv2.VideoWriter('TestVideo.mp4',fourcc,10,(640,480))
    
    for i in range(2): #Sim hasta:(a) todos los UAV llegaron, o, (b) targets agotados
        for i in range(50):
            print("Actualización: "+str(i)+", en iteracion actual")
            cellsMet=True #booleano que indica si los objetivos fueron alcanzados en todas las celdas
            placesMetIndex=[] #lista de indices de objetivos alcanzados para eliminación en ciclo final
            for celdaActual in range(1,div**2+1): #recorrido sobre todas las celdas
                asignados=0 #cantidad de UAVs asignados en celda de iteracion actual
                distancias=[] #vector de distancias actuales entre asignados y objetivos
                [CurrentCellInfo,aNumber,indicesUAVinCell,placesInCellIndex]=GRIDFcns.uavAndTargetInCell(celdaActual,initialUAVs,places,C,radOper,div)
                currentRow=div-1-(celdaActual-1)//div
                currentColumn=(celdaActual-1)%div

                deltaMatrix[(currentRow+1)*2-1][currentColumn]=len(CurrentCellInfo)-2*aNumber #calculo de delta local
                if currentRow !=0: #calculo de delta columna
                    deltaMatrix[currentRow*2,currentColumn]=deltaMatrix[(currentRow-1)*2,currentColumn]+deltaMatrix[(currentRow-1)*2+1,currentColumn]
                
                ''' ############################  Revision de la celda cuando hay UAVs presentes  ############################ '''
                if aNumber!=0:
                    GRIDFcns.initialScatter(places,initialUAVs,initialUAVsZero,div,radOper,C,autom,video)                
                    if len(CurrentCellInfo)-aNumber<aNumber:
                        asignados=len(CurrentCellInfo)-aNumber
                    else:
                        asignados=aNumber
                    
                    #vector de distancias con max match entre UAV's y objetivos
                    distancias=np.array(CurrentCellInfo[aNumber:aNumber+asignados])-np.array(CurrentCellInfo[0:aNumber])[:,[0,1]]
                    normas=np.linalg.norm(distancias,axis=1)
                    normasMatrix=np.c_[normas,normas] #duplicar columnas para operacion punto a punto con distancias
                    vunit=np.divide(distancias,normasMatrix) #vector unitario de movimiento UAV-lugar
                    #corrección para problemas con división por cero y Nan resultante
                    vunit=np.nan_to_num(vunit)
                    dx=vunit*dt #vector de movimiento según dt
                    dxnorm=np.linalg.norm(dx,axis=1)
                    arrivingBool=dxnorm*dt>=normas*dt #vector de booleanos para movimiento de llegada
                    arrivingBoolMatrix=np.c_[arrivingBool,arrivingBool] #matriz de booleanos para operaciones de movimiento
                    rowIndex=np.array(range(asignados))
                    colIndex=np.array([0,1])
                    
                    #vector de movimiento para llegada, se asigna la distancia del objetivo actual
                    moveLlegadas= np.c_[CurrentCellInfo[aNumber:aNumber+asignados]*arrivingBoolMatrix,np.transpose(np.zeros((1,distancias.shape[0]))+arrivingBool)] 
                    #vector de movimiento diferencial, se asigna la suma de la posición actual y el movimiento calculado
                    moveDistancias= CurrentCellInfo[0:aNumber]*(np.c_[arrivingBoolMatrix,arrivingBool]-1)*(-1)+ np.c_[dx*(arrivingBoolMatrix-1)*(-1),np.zeros((distancias.shape[0],1))]
                    CurrentCellInfo[0:aNumber]=moveLlegadas + moveDistancias #Suma exclusiva de actualización

                    if arrivingBool.all()==True:
                        cellsMet=cellsMet and True  #celda actual satisface asignacion
                        placesMetIndex.append(placesInCellIndex)
                    else:
                        cellsMet=cellsMet and False #celda actual no ha trasladado a sus Drones
                        placesMetIndex=[]

                    print("Celda: "+ str(celdaActual)+ "moveLlegadas es: ")
                    print(arrivingBool)

                    initialUAVs[indicesUAVinCell]=CurrentCellInfo[0:aNumber] #actualizacion en informacion global
            if video:
                #Transformar figura a imagen (no pude implementar FuncAnimation)
                img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
                img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
                theVideo.write(img)
                
    #            for celdaActual=1:div-1:#Recorrido ultima fila (actualizacion delta columnas siguientes
    #                    deltaRight(div-celdaActual)= deltaRight(div-celdaActual+1)+deltaMatrix(2*div,div-celdaActual+1)+deltaMatrix(2*div-1,div-celdaActual+1)
        placesMet=np.append((placesMet,places[np.matrix.flatten(np.array(placesMetIndex))])) #guardado de lugares alcanzados
        places=np.delete(places,placesMetIndex) #eliminacion de objetivos alcanzados
        iterations=iterations+1
    ####################################################################################################################################################
    ##  FIN                                 Simulacion de asignacion Monotonica GRID target Assgmt (Densidad Actual)
    ####################################################################################################################################################
print("Todas las celdas alcanzadas: " +str(cellsMet))
print("Terminado")
print("InitialUAVs:")
print(initialUAVs)

