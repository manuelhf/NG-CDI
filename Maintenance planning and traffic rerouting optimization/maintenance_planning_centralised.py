from ctypes import c_double
from hashlib import new
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from gurobipy import *


def maintenance_planning_centralised(Services, Predicted_RUL_matrix, ids2, Predicted_RUL_arcs):
    def findTuple(elem):
        #for t in arcs_sol_2[kl]:
        for t in arcs_sol_kl:
            if t[0]==elem:
                return t
        return None
    def all_simple_paths(G, source, target, cutoff=None):
        if source not in G:
            raise nx.NetworkXError('source node %s not in graph'%source)
        if target not in G:
            raise nx.NetworkXError('target node %s not in graph'%target)
        if cutoff is None:
            cutoff = len(G)-1
            return _all_simple_paths_graph(G, source, target, cutoff=cutoff)

    def _all_simple_paths_graph(G, source, target, cutoff=None):
        if cutoff < 1:
            return
        visited = [source]
        stack = [iter(G[source])]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.pop()
            elif len(visited) < cutoff:
                if child == target:
                    yield visited + [target]
                elif child not in visited:
                    visited.append(child)
                    stack.append(iter(G[child]))
            else: #len(visited) == cutoff:
                if child == target or target in children:
                    yield visited + [target]
                stack.pop()
                visited.pop()
    from optimisation_initialisation_centralised import H2, nodes, n, Pred_main_time, Pred_main_cost, Reac_main_time, Reac_main_cost
    # 1. Input parameters
    #n=len(Topology_matrix)
    print('0')
    T=len(Predicted_RUL_matrix[0])
    global time_periods
    time_periods=np.arange(0,T)
    d_step=1
    #Sources and sinks of connections:
    sources=np.squeeze(np.asarray(Services[:,0]))
    sinks=np.squeeze(np.asarray(Services[:,1]))
    #[7,12,14]
    kl_set=np.arange(0,len(sources))
    #demand
    d= [[400 for x in range(len(kl_set))] for y in range(len(time_periods))] 
    print('1')
    # 2. Create different sets of arcs required for optimisation
    #Arcs that lie on a possible path from source to sink for this specific connection:
    arcs=[]
    arcs_all_dupl=[]
    for kl in kl_set:
        #print('1.1')
        paths_kl = nx.all_simple_paths(H2, source=sources[kl], target=sinks[kl])    
        #print('1.2')
        arcs_kl=[]
        for i in list(paths_kl):
            for j in np.arange(0,len(i)-1):
                arcs_kl.append((i[j],i[j+1]))
                arcs_all_dupl.append((i[j],i[j+1]))
        arcs_kl_no_duplicates=list(dict.fromkeys(arcs_kl))
        #print('1.3')
        arcs.append(arcs_kl_no_duplicates)
    


    global arcs_all
    arcs_all=list(dict.fromkeys(arcs_all_dupl))
    #print(arcs_all)
    #print(arcs)

    #arcs_all=[(3, 43), (43, 0), (0, 18), (18, 21), (18, 1), (1, 21), (18, 22), (22, 1), (0, 19), (19, 18), (0, 17), (17, 1), (1, 18), (1, 22), (22, 18), (0, 1), (3, 8), (8, 82), (82, 80), (80, 72), (72, 7), (7, 71), (71, 70), (70, 59), (59, 6), (6, 62), (62, 61), (61, 69), (69, 0), (6, 68), (68, 10), (10, 0), (6, 61), (6, 0), (70, 60), (60, 6), (70, 6), (7, 79), (79, 70), (7, 0), (7, 6), (80, 6), (6, 59), (59, 70), (70, 71), (71, 7), (70, 79), (79, 7), (6, 60), (60, 70), (6, 7), (6, 70), (80, 81), (81, 73), (73, 7), (73, 74), (74, 7), (8, 0), (8, 10), (10, 68), (68, 6), (6, 80), (8, 7), (7, 73), (73, 81), (81, 80), (7, 72), (72, 80), (7, 74), (74, 73), (8, 6), (8, 83), (83, 91), (91, 0), (91, 9), (9, 0), (8, 84), (84, 91), (8, 80), (3, 2), (2, 29), (29, 1), (1, 17), (17, 0), (1, 0), (2, 27), (27, 1), (2, 28), (28, 1), (3, 0), (3, 4), (4, 52), (52, 5), (5, 2), (5, 55), (55, 2), (4, 47), (47, 2), (4, 53), (53, 5), (4, 5), (3, 6), (10, 8), (6, 8), (80, 82), (82, 8), (80, 8), (7, 8), (3, 20), (20, 1), (3, 30), (30, 2), (21, 1), (1, 29), (29, 2), (2, 55), (55, 5), (5, 54), (2, 5), (2, 47), (47, 4), (2, 3), (2, 30), (30, 3), (1, 27), (27, 2), (1, 28), (28, 2), (1, 20), (20, 3), (0, 43), (43, 3), (0, 8), (8, 3), (0, 91), (91, 84), (84, 8), (91, 83), (83, 8), (0, 3), (0, 7), (0, 10), (0, 9), (9, 91), (6, 3), (5, 56), (0, 69), (69, 61), (61, 62), (62, 6), (61, 6), (0, 6), (18, 19), (19, 0), (18, 0), (21, 18), (5, 52), (52, 4), (4, 3), (5, 4), (5, 53), (53, 4), (4, 48), (5, 57), (5, 58), (2, 31), (2, 32), (1, 23), (2, 33), (38, 39), (39, 3), (1, 24), (38, 3), (38, 37), (37, 3), (2, 34), (2, 35), (37, 38), (1, 25), (39, 38), (1, 26), (2, 36), (40, 3), (41, 3), (42, 3), (44, 3), (7, 75), (7, 76), (76, 75), (45, 3), (75, 76), (46, 3), (7, 77), (11, 0), (12, 0), (4, 49), (13, 0), (4, 50), (14, 0), (4, 51), (15, 0), (16, 0), (7, 78), (6, 63), (64, 6), (8, 85), (65, 6), (8, 86), (66, 6), (8, 87)]



    print('1.2')
    arcs_both=[]
    arcs_single=[]
    for a in arcs_all:
        if a[::-1] in arcs_all:
            if a[::-1] not in arcs_both:
                arcs_both.append(a)
        else:
            arcs_single.append(a)

    arcs_all_no_arcs=[]
    for kl in kl_set:
        arcs_all_no_arcs.append([item for item in arcs_all if item not in arcs[kl]])

    arcs_set=np.arange(0,len(arcs_all))
    arcs_both_set=np.arange(0,len(arcs_both))
    #arcs_single_set=np.arange(0,len(arcs_single))

    

    #3. Disruption (links and nodes that are subject to failure):
    global disr_arcs_2, disr_arcs_2_reverse
    disr_arcs_2=ids2
    disr_arcs_2_reverse= [arc[::-1] for arc in disr_arcs_2]
    disr_arcs=disr_arcs_2

     #p_a=np.zeros((4,T))

    # Input parameters:
    #prev_main_a=[-5,-7,-2,-5]
    #prev_main_v=[-3,-10,-8,-3]
    #C_rea_a=[150,150,150,150]
    #C_pre_a=[100,100,100,100]
   #t_rea_a=[5,5,5,5]
    #t_pre_a=[3,3,3,3]

    disr_arcs_2_set=np.arange(0,len(disr_arcs_2))

    global disr_nodes
    disr_nodes=[]
    bar_t=[]
    p_v=[]
    C_rea_v=[]
    C_pre_v=[]
    t_rea_v=[]
    t_pre_v=[]
    p_a=[]
    bar_t_a=[]
    C_rea_a=[]
    C_pre_a=[]
    t_rea_a=[]
    t_pre_a=[]
    for i in ids2:
        a=(-Predicted_RUL_arcs[ids2.index(i),:]+8)/21
        a[a < 0] = 0
        if not np.all((a == 0)):
            #disr_nodes.append(i)
            p_a.append(a.tolist())
            bar_t_a.append(next((i for i, x in enumerate(a.tolist()) if x), None)+8)
            C_rea_a.append(Reac_main_cost)
            C_pre_a.append(Pred_main_cost)
            t_rea_a.append(Reac_main_time)
            t_pre_a.append(Pred_main_time)




    for i in range(92):
        a=(-Predicted_RUL_matrix[i,:]+8)/21
        a[a < 0] = 0
        #print(a)
        if not np.all((a == 0)):
            disr_nodes.append(i)
            p_v.append(a.tolist())
            bar_t.append(next((i for i, x in enumerate(a.tolist()) if x), None)+8)
            # Input parameters:
            #C_rea_v=[150,150,150,150]
            #C_pre_v=[100,100,100,100]
            #t_rea_v=[5,5,5,5]
            #t_pre_v=[3,3,3,3]
            C_rea_v.append(Reac_main_cost)
            C_pre_v.append(Pred_main_cost)
            t_rea_v.append(Reac_main_time)
            t_pre_v.append(Pred_main_time)
            
    Prev_main=Predicted_RUL_matrix[:,0]-101
    Prev_main_a=Predicted_RUL_arcs[:,0]-101
    #print(disr_nodes)
    prev_main_v=np.take(Prev_main,disr_nodes)
    prev_main_a=Prev_main_a
    #print(disr_nodes)
    #print(p_v)
    #print(p_v[0][5])
    #print(t_pre_v)
 

    disr_nodes_set=np.arange(0,len(disr_nodes))



    for i in range(len(disr_nodes)):
        new_disr_arcs=[(pointsFrom, pointsTo) for (pointsFrom, pointsTo) in arcs_all if (disr_nodes[i]==pointsTo or disr_nodes[i]==pointsFrom)]
        disr_arcs=disr_arcs+new_disr_arcs

    disr_arcs_set=np.arange(0,len(disr_arcs))


    # 4. Optimization model:
    m = Model('Rerouting_model')

    # 4.1 Optimisation model - Decision variables:
    x = m.addVars(time_periods, kl_set, arcs_all, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="x")
    wa = m.addVars(time_periods, disr_arcs_2, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="wa")
    Ia=m.addVars(time_periods,disr_arcs_2, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="Ia")
    za=m.addVars(time_periods, disr_arcs_2, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="za")
    wv = m.addVars(time_periods, disr_nodes, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="wv")
    Iv=m.addVars(time_periods,disr_nodes, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="Iv")
    zv=m.addVars(time_periods, disr_nodes, lb=0.0, ub=GRB.INFINITY, vtype=GRB.BINARY, name="zv")

    m.modelSense = GRB.MINIMIZE

    # 4.2 Optimisation model - Capacity constraints:
    # capacity constraints
    m.addConstrs(
        (quicksum(x[t,kl,arcs_all[a][0],arcs_all[a][1]] for kl in kl_set)<=H2.get_edge_data(*arcs_all[a])['capacity'] for t in time_periods for a in arcs_set), "c1")
    # no capacity at the arc if it is failed

    m.addConstrs(
        (quicksum(x[t,kl,arcs_both[a][0],arcs_both[a][1]]+x[t,kl,arcs_both[a][1],arcs_both[a][0]] for kl in kl_set)<=H2.get_edge_data(*arcs_both[a])['capacity'] for t in time_periods for a in arcs_both_set), "c1.2")
    # no capacity at the arc if it is failed

    m.addConstrs(
        (quicksum(x[t,kl,disr_arcs_2[a][0],disr_arcs_2[a][1]] for kl in kl_set)<=(1-wa[t,disr_arcs_2[a][0],disr_arcs_2[a][1]])*H2.get_edge_data(*disr_arcs_2[a])['capacity']
        for a in disr_arcs_2_set for t in time_periods), "c2.1")

    m.addConstrs(
        (quicksum(x[t,kl,a[0],a[1]] for kl in kl_set)<=(1-wv[t,disr_nodes[v]])*H2.get_edge_data(*a)['capacity']
        for v in disr_nodes_set for a in [edge for edge in H2.out_edges(disr_nodes[v]) if edge in arcs_all]+[edge for edge in H2.in_edges(disr_nodes[v]) if edge in arcs_all] for t in time_periods), "c2.1v")

    # demand
    m.addConstrs(
        (quicksum(x[t,kl,a[0],a[1]] for a in [edge for edge in H2.in_edges(v) if edge in arcs_all])<=d[t][kl]
        for t in time_periods for kl in kl_set for v in nodes), "c30")

    #m.addConstrs(
      #  (quicksum(x[t,kl,a[0],a[1]] for a in [edge for edge in H2.out_edges(sources[kl]) if edge in arcs_all])==d[t][kl] 
     #   for t in time_periods for kl in kl_set), "c3")

    # flow conservation

    m.addConstrs(
        (quicksum(x[t,kl,a[0],a[1]] for a in [edge for edge in H2.in_edges(v) if edge in arcs_all])==quicksum(x[t,kl,a[0],a[1]] for a in [edge for edge in H2.out_edges(v) if edge in arcs_all])
        for t in time_periods for kl in kl_set for v in [v for v in nodes if ((v!=sources[kl]) & (v!=sinks[kl]))]), "c4")

    #m.addConstrs(
        #(quicksum(x[t,kl,a[0],a[1]] for a in H2.out_edges(sinks[kl]))==0
        #for t in time_periods for kl in kl_set), "c5")

    m.addConstrs(
        (quicksum(x[t,kl,a[0],a[1]] for a in arcs_all_no_arcs[kl])==0
        for t in time_periods for kl in kl_set), "c6")

    m.addConstrs(
        (Ia[t,disr_arcs[a][0],disr_arcs[a][1]]==quicksum(za[s,disr_arcs_2[a][0],disr_arcs_2[a][1]] for s in range(t+1))
        for a in disr_arcs_2_set for t in time_periods), "c7")

    m.addConstrs(
        (Iv[t,disr_nodes[v]]==quicksum(zv[s,disr_nodes[v]] for s in range(t+1))
        for v in disr_nodes_set for t in time_periods), "c7v")

    m.addConstrs(
        ((quicksum(wa[t,disr_arcs_2[a][0],disr_arcs_2[a][1]] for t in time_periods)*d_step-t_pre_a[a])*Ia[T-1,disr_arcs[a][0],disr_arcs[a][1]]==0
        for a in disr_arcs_2_set), "c8")

    m.addConstrs(
        ((quicksum(wv[t,disr_nodes[v]] for t in time_periods)*d_step-t_pre_v[v])*Iv[T-1,disr_nodes[v]]==0
        for v in disr_nodes_set), "c8v")

    m.addConstrs(
        (quicksum(za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]] for t in time_periods)<=1
        for a in disr_arcs_2_set), "c9")

    m.addConstrs(
        (quicksum(zv[t,disr_nodes[v]] for t in time_periods)<=1
        for v in disr_nodes_set), "c9v")

    m.addConstrs(
        (za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]]>=wa[t,disr_arcs_2[a][0],disr_arcs_2[a][1]]-wa[t-1,disr_arcs_2[a][0],disr_arcs_2[a][1]]
        for a in disr_arcs_2_set for t in time_periods[1:]), "c10")

    m.addConstrs(
        (zv[t,disr_nodes[v]]>=wv[t,disr_nodes[v]]-wv[t-1,disr_nodes[v]]
        for v in disr_nodes_set for t in time_periods[1:]), "c10v")

    m.addConstrs(
        (za[time_periods[0],disr_arcs_2[a][0],disr_arcs_2[a][1]]>=wa[time_periods[0],disr_arcs_2[a][0],disr_arcs_2[a][1]]
        for a in disr_arcs_2_set), "c11")

    m.addConstrs(
        (zv[time_periods[0],disr_nodes[v]]>=wv[time_periods[0],disr_nodes[v]] for v in disr_nodes_set), "c11v")
    # no capacity at the arc if it is failed
  

    # Input parameters:
    w_penalty=0.05
    w_lost=1
    w_pred=0.05
    w_reac=1000
    w_demand=0.05*0.05

    c_d=1
    c_p_pre=25
    c_lb=0.5
    c_ll=1000

    c_p_rea=1.5*c_p_pre

    #4.3 Optimisation - Objective function:
    Original_solution_matrix=pd.read_csv('original_solution.csv', index_col=0) 
    Original_solution_matrix=Original_solution_matrix.to_numpy()
    original_routes=np.squeeze(np.zeros((len(kl_set),n)))

    obj0=0
    for t in time_periods:
        for a in arcs_set:
            for kl in kl_set:
                original_routes[kl,:]=Original_solution_matrix[kl,2:n+2]
                if original_routes[kl,arcs_all[a][0]]==arcs_all[a][1]:
                    obj0=obj0+1-x[t,kl,arcs_all[a][0],arcs_all[a][1]]/400
                else:
                    obj0=obj0+x[t,kl,arcs_all[a][0],arcs_all[a][1]]/400

    obj_reac_main=0
    for v in disr_nodes_set:
        #obj_reac_main=obj_reac_main+w_reac*C_rea_v[v]*(1-Iv[min(bar_t[v],T-1),disr_nodes[v]])/(bar_t[v]-prev_main_v[v])
        #obj_reac_main=obj_reac_main+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]])*(c_p + t_rea_v[v]*(c_d+c_lb))
        obj_reac_main=obj_reac_main+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]])*(c_p_rea + t_rea_v[v]*c_lb)
        #obj_reac_main=obj_reac_main+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]])*c_d*t_rea_v[v]*quicksum(x[bar_t[v],kl,a[0],a[1]] for kl in kl_set for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all])
        obj_reac_main=obj_reac_main+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]])*c_d*quicksum(x[t,kl,a[0],a[1]] for t in range(bar_t[v],bar_t[v]+t_rea_v[v]) for kl in kl_set for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all])
    for a in disr_arcs_2_set:
        obj_reac_main=obj_reac_main+(1-Ia[min(bar_t_a[a],T-1),disr_arcs[a][0],disr_arcs[a][1]])*(c_p_rea + t_rea_a[a]*c_lb)
        #obj_reac_main=obj_reac_main+(1-Ia[min(bar_t_a[a],T-1),disr_arcs[a][0],disr_arcs[a][1]])*c_d*t_rea_a[a]*quicksum(x[bar_t_a[a],kl,disr_arcs[a][0],disr_arcs[a][1]] for kl in kl_set)
        obj_reac_main=obj_reac_main+(1-Ia[min(bar_t_a[a],T-1),disr_arcs[a][0],disr_arcs[a][1]])*c_d*quicksum(x[t,kl,disr_arcs[a][0],disr_arcs[a][1]] for t in range(bar_t_a[a],bar_t_a[a]+t_rea_a[a]) for kl in kl_set)


    m.setObjective(w_pred*obj0 + obj_reac_main
        +w_penalty*(quicksum(H2.get_edge_data(*arcs_all[a])['weight']*x[t,kl,arcs_all[a][0],arcs_all[a][1]]/400 for t in time_periods for a in arcs_set for kl in kl_set))
                    #+ quicksum(w_pred*za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]]*C_pre_a[a]/(t-prev_main_a[a]) for a in disr_arcs_2_set for t in time_periods)
                    #+ quicksum(p_a[a,t]*(1-Ia[t,disr_arcs_2[a][0],disr_arcs_2[a][1]])*(C_rea_a[a]+quicksum(x[s,kl,arcs_all[a][0],arcs_all[a][1]] for s in [s_t for s_t in range(t,t+t_rea_a[a]) if s_t <T] for kl in kl_set)) for a in disr_arcs_2_set for t in time_periods)
        #+ quicksum(w_pred*zv[t,disr_nodes[v]]*C_pre_v[v]/(t-prev_main_v[v]) for v in disr_nodes_set for t in time_periods)
        + quicksum(zv[t,disr_nodes[v]]*(c_p_pre+t_pre_v[v]*c_lb+c_ll/(t-prev_main_v[v]))  for v in disr_nodes_set for t in time_periods)
        + quicksum(za[t,disr_arcs[a][0],disr_arcs[a][1]]*(c_p_pre+t_pre_a[a]*c_lb+c_ll/(t-prev_main_a[a]))  for a in disr_arcs_2_set for t in time_periods)            
                    #+ quicksum(p_v[v][t]*(1-Iv[t,disr_nodes[v]])*(C_rea_v[v]+w_lost*quicksum(x[s,kl,a[0],a[1]] for s in [s_t for s_t in range(t,t+t_rea_v[v]) if s_t <T] for kl in kl_set for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all])) for v in disr_nodes_set for t in time_periods)
        +w_demand*c_d*quicksum(400-(quicksum(x[t,kl,a[0],a[1]]  for a in [edge for edge in H2.in_edges(sinks[kl])])) for kl in kl_set for t in time_periods))

    #Optimality Gap
    m.setParam('MIPGap', 0)
    # Solve optimisation problem

    m.optimize()



    # 5. Output:
    maintenance_plan_vector=np.ones((n,1))
    maintenance_plan_vector=-maintenance_plan_vector
    for v in disr_nodes:
        maint_time=-5
        for t in time_periods:
            if zv[t,v].x>=1:
                maint_time=t
        #if maint_time==-5:
            #print([zv[t,v].x for t in time_periods])
            #print([wv[t,v].x for t in time_periods])
        maintenance_plan_vector[v]=maint_time
    np.savetxt("foo2.csv", np.transpose(maintenance_plan_vector), delimiter=",")
    
    Routes=np.zeros((5000,n+2))
    s=len(kl_set)
    current_routes=np.zeros((len(kl_set),n))
    #Routes = np.array(([]))
    x_sol = np.zeros((len(time_periods),len(kl_set),len(arcs_set)))
    output2=open("x_2.csv", "w")
    output8=open("Routes.csv", "w")
    output8.write( 'Main plan'  '\n')
    output8.write(str(np.transpose(maintenance_plan_vector)) + '\n')
    output2.write('t'  + ';' + 'source(k)' + ';'+'sink(l)' + ';' + 'routes' ';' + 'flow' +  '\n')
    output8.write( 'Route-vector'  '\n')
    for t in time_periods:
        #print(t)
        arcs_sol=[]
        arcs_sol_2=[]
        arcs_sol_2_reverse=[]
        for kl in kl_set:
            arcs_sol_kl=[]
            for a in arcs_set:
                x_sol[t,kl,a]=x[t,kl,arcs_all[a][0],arcs_all[a][1]].x
                if x[t,kl,arcs_all[a][0],arcs_all[a][1]].x>0.1:
                    arcs_sol_kl.append((arcs_all[a][0],arcs_all[a][1]))
                    arcs_sol.append((arcs_all[a][0],arcs_all[a][1]))
            arcs_sol_2.append(arcs_sol_kl)
            arcs_sol_2_reverse.append([arc[::-1] for arc in arcs_sol_kl])

            routes = []
            startRoutes = list(filter(lambda elem: elem[0]==sources[kl], arcs_sol_kl))
            for i in range(len(startRoutes)):
                tempList = []
                currentTuple = startRoutes [i]
                #print(t,kl,currentTuple,arcs_sol_kl)
                tempList.append(currentTuple[0])
                tempList.append(currentTuple[1])
                while True:
                    if currentTuple[1]==sinks[kl]:
                        break
                    else:
                        #print([x[t,kl,a[0],a[1]].x for a in arcs_sol_kl])
                        #print(t,kl,arcs_sol_kl)
                        nextTuple = findTuple(currentTuple[1])
                        #print(nextTuple)
                        currentTuple = nextTuple
                        tempList.append(currentTuple[1])
                routes.append(tempList)
            flow=[]
            for i in range(len(routes)):
                min_flow=min(x[t,kl,routes[i][j],routes[i][j+1]].x for j in range(len(routes[i])-1))
                flow.append(int(min_flow))
            x_sol_2 = str(t) + ';' + str(sources[kl]) + ';'+ str(sinks[kl]) + ';' + str(routes) +';' + str(flow)
            output2.write(x_sol_2 + '\n')
            vect=np.ones((n,1))
            vect=-vect
            for i in range(len(routes)):
                for j in range(len(routes[i])-1):
                    vect[routes[i][j]]=routes[i][j+1]
            if t==0:
                Routes[kl,0]=0
                Routes[kl,1]=kl
                Routes[kl,2:n+2]=np.transpose(vect)
                current_routes[kl,:]=np.transpose(vect)
                route_sol = Routes[kl,:]
                output8.write(str(route_sol)  + '\n')
            else:
                if (np.not_equal(np.transpose(vect),current_routes[kl,:])).any():
                    #s=len(Routes)
                    vect_2=np.zeros((n+2,1))
                    vect_2=np.transpose(vect_2)
                    vect_2[0,2:n+2]=np.transpose(vect)
                    #vect_2[0]=t
                    #vect_2[0,0]=t-4
                    vect_2[0,0]=t
                    vect_2[0,1]=kl
                    Routes[s,:]=vect_2
                    s=s+1
                    current_routes[kl,:]=np.transpose(vect)
                    route_sol = str(t) + ';' + str(kl) + ';'+ str(np.transpose(vect)) 
                    output8.write(str(route_sol)  + '\n')
    #output results to files:
    np.savetxt("foo.csv", Routes, delimiter=",")
    output3=open("wa.csv", "w")
    output3.write( 'arc a from' ';' + 'arc a to' ';' + 'time_period' + '\n')
    output4=open("wv.csv", "w")
    output4.write( 'node' ';'  + 'time_period' + '\n')
    output5=open("zv.csv", "w")
    output5.write( 'node' ';'  + 'time_period' + '\n')
    wv_nodes=[]
    wv_time_periods=[]
    wa_arcs=[]
    wa_time_periods=[]
    wa_sol = np.zeros((len(time_periods),len(disr_arcs_2_set)))
    for a in disr_arcs_2_set:
        time_period_sol=[]
        for t in time_periods:
            wa_sol[t,a]=wa[t,disr_arcs_2[a][0],disr_arcs_2[a][1]].x
            if wa[t,disr_arcs_2[a][0],disr_arcs_2[a][1]].x==1:
                time_period_sol.append(int(t))
        if time_period_sol!=[]:
            wa_sol2 =  str(disr_arcs_2[a][0]) +';' + str(disr_arcs_2[a][1]) + ';' + str(time_period_sol)
            output3.write(wa_sol2 + '\n')
            wa_arcs.append('('+str(disr_arcs_2[a][0]) +',' + str(disr_arcs_2[a][1])+')')
            wa_time_periods.append(str(time_period_sol))      

    wv_sol = np.zeros((len(time_periods),len(disr_nodes_set)))
    for v in disr_nodes_set:
        time_period_sol=[]
        time_period_sol_2=[]
        for t in time_periods:
            wv_sol[t,v]=wv[t,disr_nodes[v]].x
            if wv[t,disr_nodes[v]].x==1:
                time_period_sol.append(int(t))
            if zv[t,disr_nodes[v]].x==1:
                time_period_sol_2.append(int(t))

        if time_period_sol!=[]:
            wv_sol2 =  str(disr_nodes[v]) +';' + str(time_period_sol)
            output4.write(wv_sol2 + '\n')
            wv_nodes.append(disr_nodes[v])
            wv_time_periods.append(str(time_period_sol))
        if time_period_sol_2!=[]:
            zv_sol =  str(disr_nodes[v]) +';' + str(time_period_sol_2)
            output5.write(zv_sol + '\n')


    obj_result=np.zeros((1,9))
    obj_result2=np.zeros((1,5))
    obj0=0
    for t in time_periods:
        for a in arcs_set:
            for kl in kl_set:
                original_routes[kl,:]=Original_solution_matrix[kl,2:n+2]
                if original_routes[kl,arcs_all[a][0]]==arcs_all[a][1]:
                    obj0=obj0+1-x[t,kl,arcs_all[a][0],arcs_all[a][1]].x/400
                else:
                    obj0=obj0+x[t,kl,arcs_all[a][0],arcs_all[a][1]].x/400
    obj_result[0,8]=w_pred*obj0
    obj_reac_main1=0
    obj_reac_main2=0
    obj_reac_main3=0
    obj_reac_main6=0
    for v in disr_nodes_set:
        obj_reac_main1=obj_reac_main1+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]].x)*(c_p_rea)
        obj_reac_main3=obj_reac_main3+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]].x)*(t_rea_v[v]*c_lb)
        obj_reac_main6=obj_reac_main6+(c_p_rea+t_rea_v[v]*c_lb)*sum(p_v[v][t]*(1-Iv[t,disr_nodes[v]].x) for t in range(1, min(bar_t[v],T-1)))
        sumsum=0
        for kl in kl_set:
            for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all]:
                sumsum=sumsum+x[bar_t[v],kl,a[0],a[1]].x
        obj_reac_main2=obj_reac_main2+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]].x)*c_d*t_rea_v[v]*sumsum

    for a in disr_arcs_2_set:
        obj_reac_main1=obj_reac_main1+(1-Ia[min(bar_t[a],T-1),disr_arcs[a][0],disr_arcs[a][1]].x)*(c_p_rea)
        obj_reac_main3=obj_reac_main3+(1-Ia[min(bar_t[a],T-1),disr_arcs[a][0],disr_arcs[a][1]].x)*(t_rea_a[a]*c_lb)
        obj_reac_main6=obj_reac_main6+(c_p_rea+t_rea_a[a]*c_lb)*sum(p_a[a][t]*(1-Ia[t,disr_arcs[a][0],disr_arcs[a][1]].x) for t in range(1, min(bar_t[a],T-1)))

    obj_result[0,5]=obj_reac_main1
    obj_result[0,3]=obj_reac_main3
    obj_result[0,0]=obj_reac_main2

    obj6=0
    for t in time_periods: 
        for a in arcs_set: 
            for kl in kl_set:
                obj6=obj6+H2.get_edge_data(*arcs_all[a])['weight']*x[t,kl,arcs_all[a][0],arcs_all[a][1]].x/400
    obj_result[0,6]=w_penalty*obj6
    
    obj1=0
    obj2=0
    obj4=0
    for v in disr_nodes_set: 
        for t in time_periods:
            obj1=obj1+zv[t,disr_nodes[v]].x*(c_ll/(t-prev_main_v[v]))
            obj2=obj2+zv[t,disr_nodes[v]].x*(t_pre_v[v]*c_lb) 
            obj4=obj4+zv[t,disr_nodes[v]].x*(c_p_pre)
    for a in disr_arcs_2_set:
        for t in time_periods:
            obj1=obj1+za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]].x*(c_ll/(t-prev_main_a[a]))
            obj2=obj2+za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]].x*(t_pre_a[a]*c_lb) 
            obj4=obj4+za[t,disr_arcs_2[a][0],disr_arcs_2[a][1]].x*(c_p_pre)

    obj_result[0,1]=obj1
    obj_result[0,2]=obj2
    obj_result[0,4]=obj4

    obj7=0
    for kl in kl_set: 
        for t in time_periods:
            obj77=0
            for a in [edge for edge in H2.in_edges(sinks[kl])]:
                obj77=obj77+x[t,kl,a[0],a[1]].x
            obj7=obj7+400-obj77

    obj_result[0,7]=c_d*obj7*w_demand

    #new
    downtime_cost=0
    for v in disr_nodes_set:
       downtime_cost= downtime_cost+(1-Iv[min(bar_t[v],T-1),disr_nodes[v]].x)*c_d*t_rea_v[v]*sum(x[bar_t[v],kl,a[0],a[1]].x for kl in kl_set for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all])
    for a in disr_arcs_2_set:
       downtime_cost= downtime_cost+(1-Ia[min(bar_t_a[a],T-1),disr_arcs[a][0],disr_arcs[a][1]].x)*c_d*t_rea_a[a]*sum(x[bar_t_a[a],kl,disr_arcs[a][0],disr_arcs[a][1]].x for kl in kl_set)

    downtime_cost2=0
    for v in disr_nodes_set:
       downtime_cost2= downtime_cost2+c_d*t_rea_v[v]*sum(p_v[v][tt]*(1-Iv[tt,disr_nodes[v]].x)*sum(x[tt,kl,a[0],a[1]].x for kl in kl_set for a in [edge for edge in H2.in_edges(disr_nodes[v]) or H2.out_edges(disr_nodes[v]) if edge in arcs_all]) for tt in range(1,min(bar_t[v],T-1)))
    for a in disr_arcs_2_set:
       downtime_cost2= downtime_cost2+c_d*t_rea_a[a]*sum(p_a[a][tt]*(1-Ia[tt,disr_arcs[a][0],disr_arcs[a][1]].x)*sum(x[tt,kl,disr_arcs[a][0],disr_arcs[a][1]].x for kl in kl_set) for tt in range(1,min(bar_t_a[a],T-1)))



    obj_result2[0,0]=obj_result[0,1]
    obj_result2[0,1]=obj_result[0,2]+obj_result[0,4]
    obj_result2[0,2]=obj_result[0,3]+obj_result[0,5]+obj_reac_main6
    obj_result2[0,3]=obj_result[0,6]
    obj_result2[0,4]=obj_result[0,7]+downtime_cost+downtime_cost2/400
    #obj_result2[0,5]=downtime_cost
    #obj_result2[0,6]=obj_reac_main6
    #obj_result2[0,7]=downtime_cost2

    output9=open("Costs.csv", "w")
    #output8.write(str(np.transpose(maintenance_plan_vector)) + '\n')
    output9.write(str(obj_result) + '\n')
    np.savetxt("Costs2.csv", obj_result, delimiter=",")
    np.savetxt("Costs_new.csv", obj_result2, delimiter=",")


    return maintenance_plan_vector, Routes, x_sol, wv_sol, wv_nodes, wv_time_periods, wa_sol, wa_arcs, wa_time_periods, obj_result