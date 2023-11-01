#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 12:24:17 2021

@author: manuelherrera
"""
import os
os.chdir("/home/manuelherrera/Working")

retval = os.getcwd()
print("Directory successfully changed", retval)

from anx import ModelUtils
from anx import Driver

import pandas as pd
import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt

###############################################################################
signal = pd.read_csv('outer_traffic_sum.csv', index_col=0) # read matrix of signals
G1 = nx.read_gml('/home/manuelherrera/Data/BT_data/backbone_outer_slice.gml')

###############################################################################
G2 = G1.to_undirected()
#for c in nx.connected_components(G2):
#    G2.subgraph(c)
    
largest_cc = max(nx.connected_components(G2), key=len)

Gc = G2.subgraph(largest_cc) 
pos = nx.spring_layout(Gc) # layout by default that it is saved for future use

nnodes = len(Gc) # 222 nodes - 206 now
nedges = Gc.number_of_edges() # 730 edges - 722 now

node_names = list(Gc.nodes); link_names = list(Gc.edges)

# initializing substring 
subs = 'core-aln1'
node_names1 = [i for i in node_names if subs in i]

G = Gc.subgraph(node_names1)

pos = nx.spring_layout(G) # layout by default that it is saved for future use

# Fixing node classifications
G.nodes['core-aln1.tan-chachalaca']['nodeType'] = 'regional'
G.nodes['core-aln1.whimsical-angelfish']['nodeType'] = 'metro'

nodes_super = [x for x,y in G.nodes(data=True) if y['nodeType']=='super']
nodes_regional = [x for x,y in G.nodes(data=True) if y['nodeType']=='regional']
nodes_metro = [x for x,y in G.nodes(data=True) if y['nodeType']=='metro']
nodes_inner = [x for x,y in G.nodes(data=True) if y['nodeType']=='super' or y['nodeType']=='regional']
nodes_outer = [x for x,y in G.nodes(data=True) if y['nodeType']=='regional' or y['nodeType']=='metro']
df_inner = signal[nodes_inner]
df_outer = signal[nodes_outer]

###############################################################################
def color_map(Graph):
    color_map_n = []
    for i in Graph.nodes():
        if Graph.nodes[i]['nodeType'] == 'super':
            color_map_n.append('red')
        elif Graph.nodes[i]['nodeType'] == 'regional':
            color_map_n.append('orange')
        elif Graph.nodes[i]['nodeType'] == 'metro':
            color_map_n.append('green')
        else: color_map_n.append('blue')
    return color_map_n
  
###############################################################################
Network2 = G.subgraph(nodes_outer)
remove = [node for node,degree in dict(Network2.degree()).items() if degree == 0]
Network = Network2.copy()
Network.remove_nodes_from(remove)

###############################################################################
color_map_n = color_map(Network)
f_outer = plt.figure(figsize=(10, 8))
plt.axis('off')
nx.draw_networkx(Network, pos, node_size=50, node_color = color_map_n, edge_color = "gray", with_labels=False)
plt.show()
#f_outer.savefig("BT_outer.pdf", bbox_inches='tight')
###############################################################################
remove_list = []
for node in remove:
    if node in df_outer.columns:
        df_outer.drop(node, axis=1, inplace=True)
        
print("Number of columns:"); print(len(df_outer.columns))
print("Number of network nodes:"); print(len(Network))
###############################################################################
df_outer.to_csv('outer_slice_traffic_1week.csv')


