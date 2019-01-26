
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
import random as rd


# In[1]:


# Data
# X coordinates
x_coordinates = np.array([82,82,82,82,82,82,82,82,82,82,                            96,50,49,13,29,58,84,14,2,3,                            5,98,84,61,1,88,91,19,93,50,                            98,5,42,61,9,80,57,23,20,85,98])

# Y coordinates
y_coordinates = np.array([76,76,76,76,76,76,76,76,76,76,                            44,5,8,7,89,30,39,24,39,82,                            10,52,25,59,65,51,2,32,3,93,                            14,42,9,62,97,55,69,15,70,60,5])

capacities = np.array([0,0,0,0,0,0,0,0,0,0,                       19,21,6,19,7,12,16,6,16,8,                       14,21,16,3,22,18,19,1,24,8,                       12,4,8,24,24,2,20,15,2,14,9])


# In[ ]:


# Stack them beside of each other
x_y_coordinates = np.column_stack((x_coordinates,                                     y_coordinates))

# Create a distance matrix from the Euclidean distance
distance_matrix = ssd.cdist(x_y_coordinates,                            x_y_coordinates,'euclidean')

# Create a distance dataframe
dist_dataframe = pd.DataFrame(distance_matrix,                              columns=[i for i in range(1,42,1)],                              index=[i for i in range(1,42,1)])
# Create a capacity dataframe
cap_dataframe = pd.DataFrame(capacities,                             columns=["Capacity"],                             index=[i for i in range(1,42,1)])


# In[5]:


# Initial solution to start with
x_0 = [24,26,22,31,11,16,25,30,34,12,14,1,20,39,15,5,36,13,18,19,32       ,38,28,10,9,23,33,21,7,4,40,35,2,17,8,6,37,3,29,27,41]


# In[13]:


def Complete_Distance_Not_Random(Dist_Array):
    
    global dist_dataframe
    
    distances = []
    
    for i in range(0,len(Dist_Array)-1,1):
        distances.append(dist_dataframe.loc[Dist_Array[i],Dist_Array[i+1]])
    
    length_of_travel = sum(distances)
    
    return length_of_travel


# In[ ]:


def Penalty_Capacity_Violation(Array,Penalty_Value, Number_Of_Trucks):
  
    # Indices of warehouse
    warehouse_index = [i for i in range(1,(2*Number_Of_Trucks)+1,1)]
    
    # Index of warehouse in the path in "Array"
    path_warehouse_index = [index                             for index,value in enumerate(Array)                             if value in warehouse_index]
    
    # "route_capacities" is list with i-th index indicative of capacity in 
    # i-th route
    route_capacities  = []
    excess_capacity =[]
    
    for k in range(len(path_warehouse_index)):
        
        if k < len(path_warehouse_index)-1:
            
            Ind_1 = Array[path_warehouse_index[k]] 
            Ind_2 = Array[path_warehouse_index[k]+1]
            
            total_capacity = 0
            
            if (Ind_2 in warehouse_index) & (Ind_1 in warehouse_index):
                pass
            else:
                route_index = Array[(path_warehouse_index[k]+1):                                          path_warehouse_index[k+1]] 
                for node in route_index: 
                    total_capacity += cap_dataframe.loc[node,'Capacity']
            
            route_capacities.append(total_capacity)  
            
            if total_capacity > 100:
                excess_capacity.append(total_capacity-100)
            else:
                excess_capacity.append(0)

    penalty = sum(excess_capacity)*Penalty_Value
    
    return penalty


# In[ ]:


def Penalty_Sequence(Array,Penalty_Value_1,Penalty_Value_2, Number_Of_Trucks):
    
    penalty = 0
    
    # Indices of warehouse
    warehouse_index = [i for i in range(1,(2*Number_Of_Trucks)+1,1)]
    
    if Array[0] not in warehouse_index: 
        penalty += Penalty_Value_1
    
    if Array[-1] not in warehouse_index:
        penalty += Penalty_Value_1
        
    if Array[1] in warehouse_index:
        penalty += Penalty_Value_1
        
    if Array[-2] in warehouse_index:
        penalty += Penalty_Value_1
        
    for i in range(len(Array)):
        if i < (len(Array)-2):
            A1 = Array[i]
            A2 = Array[i+1]
            A3 = Array[i+2]
            if (A1 in warehouse_index) and             (A2 in warehouse_index) and (A3 in warehouse_index):
                penalty += Penalty_Value_2
                
    return penalty


# In[ ]:


def Penalty_End_Points(Array,Penalty_Value, Number_Of_Trucks):
    
    penalty = 0
    
    # Indices of warehouse
    warehouse_index = [i for i in range(1,(2*Number_Of_Trucks)+1,1)]
    
    if Array[0] not in warehouse_index:
        penalty += Penalty_Value
    
    if Array[-1] not in warehouse_index:
        penalty += Penalty_Value

    return penalty

