import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from gurobipy import *

from optimisation_initialisation_centralised import optimisation_initialisation_centralised
from maintenance_planning_centralised import maintenance_planning_centralised
from visualisation_centralised_v2 import visualisation_centralised_v2

#Define inputs
#1. for initialisation

from define_network_regional_metro import*
#from define_simulated_large_network import*

Traffic_distribution_parameters=np.matrix([1,0.05])

pred_main_cost=100
pred_main_time=10
reac_main_cost=150
reac_main_time=20

#INITIALISATION
optimisation_initialisation_centralised(G1, Traffic_distribution_parameters, pred_main_cost, pred_main_time, reac_main_cost, reac_main_time)

#Define inputs
#2. for optimisation

#For the case of 5 services (0)
Services=np.matrix([
    [22, 79], [17, 47], [55, 91], [63, 30], [43, 69]])

#Services=np.matrix([
    #[3, 21], [6, 54], [8, 56], [2, 71], [1, 48], [43, 57], [20, 58], [30, 22], [10, 31],
    #[17, 32], [80, 23], [91, 33], [38, 24], [9, 34], [19, 35], [37, 25], [39, 26], [69, 36], [40, 72], [41, 73], [42, 74], [44, 75], 
    #[45, 76], [46, 77], [11, 47], [12, 49], [13, 50], [14, 51], [15, 52], [16, 53], [27, 81], [28, 59], [70, 55], [60, 78], [61, 79], [62, 82], 
    #[68, 83], [84, 63], [64, 85], [65, 86], [66, 87]])

#For the case of 5 services (0)
#ids =  [11,  1,  18, 0,  24, 7,  5,  2,  4,  35, 56]
#ruls = [52,  81, 87, 89, 93, 96, 41, 47, 49, 33, 72]

#For the case of 5 services (case including arcs)
ids =  [0, 1, 2, 4, 8, 18]
ruls = [89, 81, 47, 49, 92, 87]
ids2 = [(55,5), (0,7), (0,6), (6,3), (70,79)]
ruls2 = [41, 96, 64, 55, 93]

#seed=54545 (1)
#ids =  [86, 88, 40, 23, 2,  77, 90, 11, 49, 31, 44, 52, 19, 37, 80, 24,  9, 61, 35, 28, 55, 10, 48, 17, 46, 15, 42,  4, 12, 71, 56, 38, 91, 20, 83, 14, 65, 59, 36, 81, 62]
#ruls = [90, 56, 78, 54, 72, 88, 67, 56, 59, 79, 88, 72, 50, 87, 53, 52, 61, 79, 51, 60, 59, 65, 79, 89, 61, 63, 64, 62, 83, 58, 74, 87, 70, 75, 58, 74, 87, 71, 88, 85, 52]
#ids2 = []
#ruls2 = []
#ids =  [71,  2,  4, 48]
#ruls = [58, 72, 62, 79]
#ids =  [2, 71]
#ruls = [72, 58]

#seed=458457 (2)
#ids = [36, 26, 78, 34, 64, 74, 90, 22, 86, 31, 4, 7, 46, 68, 30, 25, 54, 10, 17, 49, 3, 5, 29, 61, 51, 43, 88, 13, 81, 35, 20, 76, 57, 27, 33, 14, 91, 62, 24, 15, 37]
#ids=[id-1 for id in ids]
#print("ids",ids)
#ruls = [80, 71, 53, 85, 64, 59, 82, 58, 63, 74, 61, 52, 85, 88, 66, 82, 65, 62, 60, 59, 86, 81, 85, 71, 59, 53, 58, 50, 76, 76, 65, 53, 67, 75, 52, 70, 57, 65, 80, 83, 64]

#seed=513031 (3)
#ids =  [91, 41, 78, 46, 77, 52, 45, 6, 65, 81, 56, 32, 15, 22, 39, 69, 75, 73, 84, 19, 34, 61, 1, 58, 26, 36, 5, 55, 35, 16, 44, 85, 38, 2, 21, 25, 29, 76, 79, 9, 83]
#ids=[id-1 for id in ids]
#ruls = [79, 60, 65, 54, 79, 56, 69, 72, 58, 59, 61, 82, 86, 84, 66, 74, 69, 62, 80, 59, 51, 56, 87, 89, 90, 77, 79, 73, 71, 89, 55, 58, 60, 87, 78, 63, 85, 71, 56, 90, 80]
#ids = [91, 41, 78]
#ids=[id-1 for id in ids]
#ruls = [79, 60, 65]
#ids =  [46, 52, 65, 81, 19, 34, 61,  44, 85, 38, 79]
#ids=[id-1 for id in ids]
#ruls = [54, 56,  58, 59, 59, 51, 56,  55, 58, 60, 56]




#seed=657849 (4)
#ids = [18, 59, 29, 47, 32, 25, 68, 11, 80, 60, 19, 44, 64, 1, 56, 40, 41, 13, 57, 46, 88, 42, 61, 12, 50, 27, 23, 77, 9, 31, 15, 66, 33, 73, 36, 71, 79, 54, 90, 52, 92]
#ids=[id-1 for id in ids]
#ruls = [83, 88, 62, 57, 59, 52, 68, 54, 88, 54, 72, 55, 89, 52, 55, 66, 86, 65, 65, 71, 51, 86, 54, 73, 71, 62, 68, 79, 64, 78, 90, 77, 81, 60, 82, 72, 50, 55, 63, 67, 55]

#seed=756733 (5)
#ids = [7, 60, 89, 3, 1, 13, 36, 26, 30, 65, 22, 91, 21, 37, 62, 75, 23, 6, 92, 53, 69, 49, 56, 18, 33, 70, 54, 46, 86, 43, 90, 4, 64, 74, 25, 8, 17, 41, 67, 58, 63]
#ids=[id-1 for id in ids]
#ruls = [53, 72, 52, 50, 59, 82, 60, 59, 87, 90, 66, 70, 57, 65, 84, 82, 75, 54, 62, 59, 71, 77, 67, 51, 75, 71, 63, 80, 82, 64, 58, 89, 86, 71, 71, 88, 63, 52, 87, 52, 65]

#seed=779771 (6)
#ids = [20, 37, 17, 74, 25, 61, 27, 16, 6, 39, 58, 4, 47, 18, 32, 65, 72, 90, 81, 51, 29, 26, 42, 79, 69, 92, 44, 83, 30, 41, 73, 38, 70, 15, 76, 46, 12, 84, 40, 64, 75]
#ids=[id-1 for id in ids]
#ruls = [65, 74, 69, 76, 75, 85, 60, 69, 79, 53, 57, 63, 79, 83, 55, 54, 59, 79, 58, 70, 66, 85, 61, 71, 76, 89, 82, 81, 77, 79, 87, 65, 76, 88, 54, 53, 67, 67, 69, 78, 66]

#seed=8236474 (7)
#ids = [88, 15, 58, 20, 35, 2, 29, 69, 22, 27, 86, 70, 41, 33, 24, 42, 83, 75, 21, 18, 39, 55, 36, 84, 6, 56, 91, 72, 5, 10, 73, 54, 64, 26, 76, 11, 87, 59, 60, 65, 68]
#ids=[id-1 for id in ids]
#ruls = [70, 68, 83, 52, 81, 53, 67, 85, 77, 80, 77, 86, 87, 56, 84, 59, 67, 79, 58, 86, 75, 54, 76, 70, 82, 69, 75, 72, 70, 66, 68, 82, 55, 73, 68, 90, 88, 77, 81, 53, 85]

m=92
Predicted_RUL_matrix=np.zeros((m,200))
Predicted_RUL_arcs=np.zeros((len(ruls2),200))
for i in ids2:
    for j in range(0,ruls2[ids2.index(i)]+1):
        Predicted_RUL_arcs[ids2.index(i),j]=ruls2[ids2.index(i)]-1*j
    Predicted_RUL_arcs[ids2.index(i),j+1]=0
    s=j+2
    for j in range(0,101):
        Predicted_RUL_arcs[ids2.index(i),j+s]=100-1*j
    Predicted_RUL_arcs[ids2.index(i),j+1+s]=0
    s=j+1+s+1
    for j in range(0,96-ruls2[ids2.index(i)]):
        Predicted_RUL_arcs[ids2.index(i),j+s]=100-1*j
for i in range(0,m):
    if i in ids:
        for j in range(0,ruls[ids.index(i)]+1):
            Predicted_RUL_matrix[i,j]=ruls[ids.index(i)]-1*j
        Predicted_RUL_matrix[i,j+1]=0
        s=j+2
        for j in range(0,101):
            Predicted_RUL_matrix[i,j+s]=100-1*j
        Predicted_RUL_matrix[i,j+1+s]=0
        s=j+1+s+1
        for j in range(0,96-ruls[ids.index(i)]):
            Predicted_RUL_matrix[i,j+s]=100-1*j
    else:
        b=random.randint(50, 90)
        for j in range(0,200):
            Predicted_RUL_matrix[i,j]=b-0.01*j


#replace with probability distributions:
#Predicted_RUL_matrix=pd.read_csv('RULS_2.csv', index_col=0) 
#Predicted_RUL_matrix=pd.read_csv('RULs_test_3.csv', index_col=0) 
#Predicted_RUL_matrix=Predicted_RUL_matrix.to_numpy()
#Predicted_RUL_matrix=Predicted_RUL_matrix.transpose()
#print(Predicted_RUL_matrix[:,50:60])

#OPTIMISATION
result=maintenance_planning_centralised(Services, Predicted_RUL_matrix[:,0:150],ids2,Predicted_RUL_arcs[:,0:150])
#maintenance_plan
#print(result[0])
#Routes
#print(result[1])
#print(result[9])

#VISUALISATION
#works for fixed number of services - 3 !!! atm
visualisation_centralised_v2(node_pos2, node_color2,Services, result)