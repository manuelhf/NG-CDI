import numpy as np
import networkx as nx

def optimisation_initialisation_centralised(Network, Traffic_distribution_parameters, pred_main_cost, pred_main_time, reac_main_cost, reac_main_time):

# 1. Read input parameters:
    H=Network
    #nx.draw(H, node_size = 50, with_labels = True)
    #plt.show()
    
    #NETWORK!!!!


    ##Network:
    #H=G
    global n
    n=len(H.nodes)
    global H2
    H2 = H.to_directed()
    global nodes
    nodes=list(H.nodes)
    global nodes_set
    nodes_set=np.arange(0,len(nodes))
    #Attributes of edges
    nx.set_edge_attributes(H2, 0.1,'weight')
    #H2[8][10]['weight']=0.09
    nx.set_edge_attributes(H2, 10000,'capacity')
    
    global Pred_main_cost
    Pred_main_cost=pred_main_cost
    global Pred_main_time
    Pred_main_time=pred_main_time
    global Reac_main_cost
    Reac_main_cost=reac_main_cost
    global Reac_main_time
    Reac_main_time=reac_main_time

    return




