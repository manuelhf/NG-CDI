import numpy as np
import networkx as nx
import math
import plotly.graph_objects as go

def visualisation_centralised_v2(node_pos, node_color2,Services, result):
    def findTuple(elem):
        for t in arcs_sol_2[kl]:
            if t[0]==elem:
                return t
        return None
    def get_color(i):
        '''Assign a color to a vertex.'''
        if i==1:
            color='pink'
        elif i==2:
            color='lightgreen'
        elif i==3:
            color='lightblue'
        elif i==4:
            color='coral'
        elif i==5:
            color='forestgreen'
        elif i==6:
            color='steelblue'
        elif i==7:
            color='gold'
        elif i==8:
            color='blueviolet'
        else:
            color='olivedrab'
        return (color) 

    x_sol=result[2]
    wv_sol=result[3]
    wv_nodes=result[4]
    wv_time_periods=result[5]
    wa_sol=result[6]
    wa_arcs=result[7]
    wa_time_periods=result[8]
    from optimisation_initialisation_centralised import H2
    print([H2.nodes[v]['community'] for v in H2.nodes])
    print([get_color(H2.nodes[v]['community']) for v in H2.nodes])
    from maintenance_planning_centralised import time_periods, disr_arcs_2, disr_arcs_2_reverse, arcs_all, disr_nodes
    sources=np.squeeze(np.asarray(Services[:,0]))
    sinks=np.squeeze(np.asarray(Services[:,1]))
    kl_set=np.arange(0,len(sources))
    arcs_set=np.arange(0,len(arcs_all))
    disr_arcs_2_set=np.arange(0,len(disr_arcs_2))
    disr_nodes_set=np.arange(0,len(disr_nodes))

    times = str(time_periods)

    # make figure
    fig_dict = {
        "data": [],
        "layout": {'showlegend': False,},
        "frames": []
    }
    fig_dict["layout"]["xaxis"] = {"domain": [0.6, 1.]}
    fig_dict["layout"]["xaxis2"] = {"domain": [0, .55], "visible": False}
    fig_dict["layout"]["yaxis2"] = {"anchor": "x2", "visible": False}
    fig_dict["layout"]["paper_bgcolor"] = "white"
    fig_dict["layout"]["plot_bgcolor"] = "white"
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        dict(
            buttons=list([
                dict(
                    args=[None, {"frame": {"duration": 100, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 0,
                                                                        "easing": "quadratic-in-out"}}],
                    label="Play",
                    method="animate"
                    ),
                dict(
                    args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="Pause",
                    method="animate"
                    ),
            ]),
            type = "buttons",
            direction="down",
            showactive=True,
            x=-0.05,
            y=0.05,
        ),
        dict(
            buttons=list([
                dict(
                    args=[{"visible": [True, True, True, True,True, True,True,True,True,True, True,True,True,True,True,True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="All connections",
                    method="update"
                    ),
                dict(
                    args=[{"visible": [True, True, True, True,False,  False,False, False,False,False, False,False,  True,True,True, True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}},
                                    ],
                    label="Connection 1",
                    method="update"
                    ),
                dict(
                    args=[{"visible": [True, True, False, False,  True,True, False,False, False, False,False,False,True,True, True,True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="Connection 2",
                    method="update"
                    ),
                dict(
                    args=[{"visible": [True, True, False, False,False,  False,True,True,False,False, False,False,True,True,True,  True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="Connection 3",
                    method="update"
                    ),
                dict(
                    args=[{"visible": [True, True, False,False,  False,False,False,False,True, True,False,False,True,True, True, True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="Connection 4",
                    method="update"
                    ),
                dict(
                    args=[{"visible": [True, True, False, False,False,  False,False,False,False,False, True,True,True,True,True,   True,True,True]}, {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    label="Connection 5",
                    method="update"
                    )                        
            ]),
            type = "buttons",
            direction="down",
            showactive=True,
            x=-0.05,
            y=0.8,

        )
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Time:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 0, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": -1.1},
        "len": 0.575,
        "x": 0,
        "y": 0.05,
        "steps": []
    }
    t=0
    arcs_sol=[]
    arcs_sol_2=[]
    arcs_sol_2_reverse=[]
    for a in H2.edges:
        H2[a[0]][a[1]]['label']=''
    for kl in kl_set:
        arcs_sol_kl=[]
        for a in arcs_set:
            if x_sol[t,kl,a]>0.1:
                if H2[arcs_all[a][0]][arcs_all[a][1]]['label']=='':
                    H2[arcs_all[a][0]][arcs_all[a][1]]['label']=str(sources[kl])+'\u2192'+str(sinks[kl])+' ['+str(int(x_sol[t,kl,a]))+']'
                else:
                    H2[arcs_all[a][0]][arcs_all[a][1]]['label']=H2[arcs_all[a][0]][arcs_all[a][1]]['label']+',  '+str(sources[kl])+'\u2192'+str(sinks[kl])+' ['+str(int(x_sol[t,kl,a]))+']'
                arcs_sol_kl.append((arcs_all[a][0],arcs_all[a][1]))
                arcs_sol.append((arcs_all[a][0],arcs_all[a][1]))
        arcs_sol_2.append(arcs_sol_kl)
        arcs_sol_2_reverse.append([arc[::-1] for arc in arcs_sol_kl])

    nx.draw_networkx_labels(H2,node_pos,font_size=15,font_color='black')
    key_list=list(node_pos.keys())
    val_list=list(node_pos.values())

    edge_x_orange = []
    edge_y_orange = []
    edge_x_green = [[] for i in range(len(kl_set))]
    edge_y_green = [[] for i in range(len(kl_set))]
    edge_x_grey = []
    edge_y_grey = []
    edge_labels= [[] for i in range(len(kl_set))]
    middle_x= [[] for i in range(len(kl_set))]
    middle_y= [[] for i in range(len(kl_set))]
    for edge in H2.edges: 
        x0, y0 = val_list[key_list.index(edge[0])]
        x1, y1 = val_list[key_list.index(edge[1])]
        flag=0
        for a2 in disr_arcs_2_set:
            if (edge==disr_arcs_2[a2] or edge==disr_arcs_2_reverse[a2]) and wa_sol[t,a2]==1:
                flag=1
        if flag==1:
            edge_x_orange.append(x0)
            edge_x_orange.append(x1)
            edge_x_orange.append(None)
            edge_y_orange.append(y0)
            edge_y_orange.append(y1)
            edge_y_orange.append(None)
        else:
            edge_x_grey.append(x0)
            edge_x_grey.append(x1)
            edge_x_grey.append(None)
            edge_y_grey.append(y0)
            edge_y_grey.append(y1)
            edge_y_grey.append(None)
            for kl in kl_set:
                if edge in arcs_sol_2[kl] or edge in arcs_sol_2_reverse[kl]:
                    if edge in arcs_sol_2_reverse[kl]:
                        x_temp=x0
                        y_temp=y0
                        x0=x1
                        x1=x_temp
                        y0=y1
                        y1=y_temp
                    l1=0.1
                    l2=math.sqrt((x0-x1)**2+(y0-y1)**2)
                    #sin_a=0.259
                    #cos_a=0.966
                    sin_a=0.139
                    cos_a=0.99
                    x3=(x0+x1)/2+l1/l2*((x0-(x0+x1)/2)*cos_a+(y0-(y0+y1)/2)*sin_a)
                    y3=(y0+y1)/2+l1/l2*((y0-(y0+y1)/2)*cos_a-(x0-(x0+x1)/2)*sin_a)
                    x4=(x0+x1)/2+l1/l2*((x0-(x0+x1)/2)*cos_a-(y0-(y0+y1)/2)*sin_a)
                    y4=(y0+y1)/2+l1/l2*((y0-(y0+y1)/2)*cos_a+(x0-(x0+x1)/2)*sin_a)
                    edge_x_green[kl].append(x0)
                    edge_x_green[kl].append(x1)
                    edge_x_green[kl].append(None)
                    edge_y_green[kl].append(y0)
                    edge_y_green[kl].append(y1)
                    edge_y_green[kl].append(None)
                    edge_x_green[kl].append(x3)
                    edge_x_green[kl].append((x0+x1)/2)
                    edge_x_green[kl].append(None)
                    edge_y_green[kl].append(y3)
                    edge_y_green[kl].append((y0+y1)/2)
                    edge_y_green[kl].append(None)
                    edge_x_green[kl].append(x4)
                    edge_x_green[kl].append((x0+x1)/2)
                    edge_x_green[kl].append(None)
                    edge_y_green[kl].append(y4)
                    edge_y_green[kl].append((y0+y1)/2)
                    edge_y_green[kl].append(None)
                    middle_x[kl].append((x0+x1)/2)
                    middle_y[kl].append((y0+y1)/2)
                    edge_labels[kl].append(H2[edge[0]][edge[1]]['label'])

        
    edge_trace_1 = go.Scatter(
        x=edge_x_orange, y=edge_y_orange,
        line=dict(width=2, color='orange'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')
        
    edge_trace_2_kl_0 = go.Scatter(
            x=edge_x_green[0], y=edge_y_green[0],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')
    edge_trace_2_kl_1 = go.Scatter(
        x=edge_x_green[1], y=edge_y_green[1],
        line=dict(width=2, color='mediumseagreen'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')

    edge_trace_2_kl_2 = go.Scatter(
        x=edge_x_green[2], y=edge_y_green[2],
        line=dict(width=2, color='mediumseagreen'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')

    edge_trace_2_kl_3 = go.Scatter(
        x=edge_x_green[3], y=edge_y_green[3],
        line=dict(width=2, color='mediumseagreen'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')

    edge_trace_2_kl_4 = go.Scatter(
        x=edge_x_green[4], y=edge_y_green[4],
        line=dict(width=1, color='mediumseagreen'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')
        
    edge_trace_3 = go.Scatter(
        x=edge_x_grey, y=edge_y_grey,
        line=dict(width=2, color='lightgrey'),
        hoverinfo='none',
        mode='lines',
        xaxis='x2', yaxis='y2')

    node_x = []
    node_y = []
    color_map = []
    color_map2 = []
    size_map=[]
    node_x_kl=[]
    node_y_kl=[]
    node_main_x=[]
    node_main_y=[]
    node_main_text=[]
    node_text_kl=[]
    for i in range(len(sources)):
        xx, yy = val_list[key_list.index(sources[i])]
        xx2, yy2 = val_list[key_list.index(sinks[i])]
        node_x_kl.append(xx+0.05)
        node_x_kl.append(xx2+0.05)
        #node_text_kl.append(f"<b>Source {str(i+1)}</b>") 
        node_text_kl.append(f"<b>Source {str(i+1)}</b>") 
        node_y_kl.append(yy+0.05)
        node_y_kl.append(yy2+0.05)
        node_text_kl.append(f"<b>Sink {str(i+1)}</b>")
    for i in range(0,9):
        xx, yy = val_list[key_list.index(i)]
        node_main_x.append(xx)
        node_main_y.append(yy)
        node_main_text.append(f"<b>{str(i)}</b>") 
    #xx, yy = val_list[key_list.index(11)]
    #node_main_x.append(xx)
    #node_main_y.append(yy)
    #node_main_text.append(f"<b>{str(11)}</b>") 
    #xx, yy = val_list[key_list.index(18)]
    #node_main_x.append(xx)
    #node_main_y.append(yy)
    #node_main_text.append(f"<b>{str(18)}</b>") 
    #xx, yy = val_list[key_list.index(24)]
    #node_main_x.append(xx)
    #node_main_y.append(yy)
    #node_main_text.append(f"<b>{str(24)}</b>") 
    #xx, yy = val_list[key_list.index(35)]
    #node_main_x.append(xx)
    #node_main_y.append(yy)
    #node_main_text.append(f"<b>{str(35)}</b>") 
    #xx, yy = val_list[key_list.index(56)]
    #node_main_x.append(xx)
    #node_main_y.append(yy)
    #node_main_text.append(f"<b>{str(56)}</b>") 


    for node in H2.nodes():
        xx, yy = val_list[key_list.index(node)]
        node_x.append(xx)
        node_y.append(yy)
        if node in disr_nodes_set and wv_sol[t,node]==1:
            color_map2.append('orange')
        else:
            color_map2.append(get_color(H2.nodes[node]['community']))
        if node in disr_nodes_set and wv_sol[t,node]==1:
            color_map.append('orange')
            if H2.nodes[node]['nodeType'] == 'regional':
                size_map.append(15)
            else:
                size_map.append(10)
        elif H2.nodes[node]['nodeType'] == 'super':
            color_map.append('steelblue')
            size_map.append(10)
        elif H2.nodes[node]['nodeType'] == 'regional':
            color_map.append('lightskyblue')
            size_map.append(15)
        elif H2.nodes[node]['nodeType'] == 'metro':
            color_map.append('mediumpurple')
            size_map.append(10)
        else:
            color_map.append('purple')
            size_map.append(7)

    node_text = []
    for node in H2.nodes:
        node_text.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        textfont_size=14,
        hoverinfo='none',
        text=node_text,
        marker=dict(
            opacity=1,
            showscale=False,
            color=color_map,
            #color=node_color2,
            size=size_map,
            line_width=2,
            line_color='grey'),
        xaxis='x2', yaxis='y2')

    node_trace_kl = go.Scatter(
        x=node_x_kl, y=node_y_kl,
        mode='markers+text',
        textfont_size=10,
        textfont_color='mediumseagreen',
        hoverinfo='none',
        text=node_text_kl,
        textposition='middle center',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')

    node_trace_main = go.Scatter(
        x=node_main_x, y=node_main_y,
        mode='markers+text',
        textfont_size=12,
        textfont_color='black',
        hoverinfo='none',
        text=node_main_text,
        textposition='middle center',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')

    node_trace_middle_kl_0 = go.Scatter(
        x=middle_x[0], y=middle_y[0],
        mode='markers',
        textfont_size=14,
        hoverinfo='text',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')
    node_trace_middle_kl_0.text=edge_labels[0]

    node_trace_middle_kl_1 = go.Scatter(
        x=middle_x[1], y=middle_y[1],
        mode='markers',
        textfont_size=14,
        hoverinfo='text',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')
    node_trace_middle_kl_1.text=edge_labels[1]

    node_trace_middle_kl_2 = go.Scatter(
        x=middle_x[2], y=middle_y[2],
        mode='markers',
        textfont_size=14,
        hoverinfo='text',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')
    node_trace_middle_kl_2.text=edge_labels[2]
    #end t=0

    node_trace_middle_kl_3 = go.Scatter(
        x=middle_x[3], y=middle_y[3],
        mode='markers',
        textfont_size=14,
        hoverinfo='text',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')
    node_trace_middle_kl_3.text=edge_labels[3]

    node_trace_middle_kl_4 = go.Scatter(
        x=middle_x[4], y=middle_y[4],
        mode='markers',
        textfont_size=14,
        hoverinfo='text',
        marker=dict(
            showscale=False,
            opacity=0,
            size=40,
            line_width=2),
            xaxis='x2', yaxis='y2')
    node_trace_middle_kl_4.text=edge_labels[4]

    fig_dict["data"].append(edge_trace_1)
    fig_dict["data"].append(edge_trace_3)
    #fig_dict["data"].append(node_trace)
    #fig_dict["data"].append(node_trace_kl)
    #fig_dict["data"].append(node_trace_main)
    fig_dict["data"].append(edge_trace_2_kl_0)
    fig_dict["data"].append(node_trace_middle_kl_0)
    fig_dict["data"].append(edge_trace_2_kl_1)
    fig_dict["data"].append(node_trace_middle_kl_1)
    fig_dict["data"].append(edge_trace_2_kl_2)
    fig_dict["data"].append(node_trace_middle_kl_2)
    fig_dict["data"].append(edge_trace_2_kl_3)
    fig_dict["data"].append(node_trace_middle_kl_3)
    fig_dict["data"].append(edge_trace_2_kl_4)
    fig_dict["data"].append(node_trace_middle_kl_4)
    fig_dict["data"].append(node_trace)
    fig_dict["data"].append(node_trace_kl)
    fig_dict["data"].append(node_trace_main)

    table1=go.Table(header=dict(values=['Node', 'Time period']),
                #cells=dict(values=[[wv_nodes[i] for i in range(len(wv_nodes))], [wv_time_periods[i] for i in range(len(wv_nodes))]]),domain=dict(x=[0.6, 1],
                cells=dict(values=[[wv_nodes[i] for i in range(len(wv_nodes))], [wv_time_periods[i] for i in range(len(wv_nodes))]],font=dict(color='black', size=9)),domain=dict(x=[0.6, 1],
                    y=[0, 0.95]))

            
    fig_dict["data"].append(table1)     

    table2=go.Table(header=dict(values=['Arc', 'Time period']),
                cells=dict(values=[[wa_arcs[i] for i in range(len(wa_arcs))], [wa_time_periods[i] for i in range(len(wa_arcs))]],font=dict(color='black', size=9)), domain=dict(x=[0.6, 1],
                    y=[0, 0.65]))

    fig_dict["data"].append(table2)   

    table3_t=[]
    table3_kl=[]
    table3_routes=[]
    table3_flow=[]

    for t in time_periods:
        print(t)
        arcs_sol=[]
        arcs_sol_2=[]
        arcs_sol_2_reverse=[]
        for a in H2.edges:
            H2[a[0]][a[1]]['label']=''
        for kl in kl_set:
            arcs_sol_kl=[]
            for a in arcs_set:
                if x_sol[t,kl,a]>0.1:
                    if H2[arcs_all[a][0]][arcs_all[a][1]]['label']=='':
                        H2[arcs_all[a][0]][arcs_all[a][1]]['label']=str(sources[kl])+'\u2192'+str(sinks[kl])+' ['+str(int(x_sol[t,kl,a]))+']'
                    else:
                        H2[arcs_all[a][0]][arcs_all[a][1]]['label']=H2[arcs_all[a][0]][arcs_all[a][1]]['label']+',  '+str(sources[kl])+'\u2192'+str(sinks[kl])+' ['+str(int(x_sol[t,kl,a]))+']'
                    arcs_sol_kl.append((arcs_all[a][0],arcs_all[a][1]))
                    arcs_sol.append((arcs_all[a][0],arcs_all[a][1]))
            arcs_sol_2.append(arcs_sol_kl)
            arcs_sol_2_reverse.append([arc[::-1] for arc in arcs_sol_kl])

            routes = []
            startRoutes = list(filter(lambda elem: elem[0]==sources[kl], arcs_sol_kl))
            for i in range(len(startRoutes)):
                tempList = []
                currentTuple = startRoutes [i]
                tempList.append(currentTuple[0])
                tempList.append(currentTuple[1])
                while True:
                    if currentTuple[1]==sinks[kl]:
                        break
                    else:
                        nextTuple = findTuple(currentTuple[1])
                        currentTuple = nextTuple
                        tempList.append(currentTuple[1])
                routes.append(tempList)
            flow=[]
            for i in range(len(routes)):
                min_flow=min(x_sol[t,kl,arcs_all.index((routes[i][j],routes[i][j+1]))] for j in range(len(routes[i])-1))
                flow.append(int(min_flow))

            table3_t.append(str(t))
            table3_kl.append(str('(' + str(sources[kl]) + ','+ str(sinks[kl]) + ')' ))
            table3_routes.append(str(routes))
            table3_flow.append(str(flow))

        arcs_sol_reverse = [arc[::-1] for arc in arcs_sol]

        nx.draw_networkx_labels(H2,node_pos,font_size=15,font_color='black')

        frame = {"data": [], "name": str(t),  "layout": {'showlegend': False}}
 
        edge_x_orange = []
        edge_y_orange = []
        edge_x_green = [[] for i in range(len(kl_set))]
        edge_y_green = [[] for i in range(len(kl_set))]
        edge_x_grey = []
        edge_y_grey = []
        edge_labels==[[] for i in range(len(kl_set))]
        middle_x=[[] for i in range(len(kl_set))]
        middle_y=[[] for i in range(len(kl_set))]

        for edge in H2.edges: 
            x0, y0 = val_list[key_list.index(edge[0])]
            x1, y1 = val_list[key_list.index(edge[1])]
            flag=0
            for a2 in disr_arcs_2_set:
                if (edge==disr_arcs_2[a2] or edge==disr_arcs_2_reverse[a2]) and wa_sol[t,a2]==1:
                    flag=1
            if flag==1:
                edge_x_orange.append(x0)
                edge_x_orange.append(x1)
                edge_x_orange.append(None)
                edge_y_orange.append(y0)
                edge_y_orange.append(y1)
                edge_y_orange.append(None)
            else:
                edge_x_grey.append(x0)
                edge_x_grey.append(x1)
                edge_x_grey.append(None)
                edge_y_grey.append(y0)
                edge_y_grey.append(y1)
                edge_y_grey.append(None)
                for kl in kl_set:
                    if edge in arcs_sol_2[kl] or edge in arcs_sol_2_reverse[kl]:
                        if edge in arcs_sol_2_reverse[kl]:
                            x_temp=x0
                            y_temp=y0
                            x0=x1
                            x1=x_temp
                            y0=y1
                            y1=y_temp
                        l1=0.1
                        l2=math.sqrt((x0-x1)**2+(y0-y1)**2)
                        #sin_a=0.259
                        #cos_a=0.966
                        sin_a=0.139
                        cos_a=0.99
                        x3=(x0+x1)/2+l1/l2*((x0-(x0+x1)/2)*cos_a+(y0-(y0+y1)/2)*sin_a)
                        y3=(y0+y1)/2+l1/l2*((y0-(y0+y1)/2)*cos_a-(x0-(x0+x1)/2)*sin_a)
                        x4=(x0+x1)/2+l1/l2*((x0-(x0+x1)/2)*cos_a-(y0-(y0+y1)/2)*sin_a)
                        y4=(y0+y1)/2+l1/l2*((y0-(y0+y1)/2)*cos_a+(x0-(x0+x1)/2)*sin_a)
                        edge_x_green[kl].append(x0)
                        edge_x_green[kl].append(x1)
                        edge_x_green[kl].append(None)
                        edge_y_green[kl].append(y0)
                        edge_y_green[kl].append(y1)
                        edge_y_green[kl].append(None)
                        edge_x_green[kl].append(x3)
                        edge_x_green[kl].append((x0+x1)/2)
                        edge_x_green[kl].append(None)
                        edge_y_green[kl].append(y3)
                        edge_y_green[kl].append((y0+y1)/2)
                        edge_y_green[kl].append(None)
                        edge_x_green[kl].append(x4)
                        edge_x_green[kl].append((x0+x1)/2)
                        edge_x_green[kl].append(None)
                        edge_y_green[kl].append(y4)
                        edge_y_green[kl].append((y0+y1)/2)
                        edge_y_green[kl].append(None)
                        middle_x[kl].append((x0+x1)/2)
                        middle_y[kl].append((y0+y1)/2)
                        edge_labels[kl].append(H2[edge[0]][edge[1]]['label'])

        edge_trace_1 = go.Scatter(
            x=edge_x_orange, y=edge_y_orange,
            line=dict(width=2, color='orange'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')

        edge_trace_2_kl_0 = go.Scatter(
            x=edge_x_green[0], y=edge_y_green[0],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')
        edge_trace_2_kl_1 = go.Scatter(
            x=edge_x_green[1], y=edge_y_green[1],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')
        edge_trace_2_kl_2 = go.Scatter(
            x=edge_x_green[2], y=edge_y_green[2],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')
        edge_trace_2_kl_3 = go.Scatter(
            x=edge_x_green[3], y=edge_y_green[3],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')
        edge_trace_2_kl_4 = go.Scatter(
            x=edge_x_green[4], y=edge_y_green[4],
            line=dict(width=2, color='mediumseagreen'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')


        edge_trace_3 = go.Scatter(
            x=edge_x_grey, y=edge_y_grey,
            line=dict(width=2, color='lightgrey'),
            hoverinfo='none',
            mode='lines',
            xaxis='x2', yaxis='y2')

        node_x = []
        node_y = []
        color_map = []
        color_map2=[]
        size_map=[]
        node_x_kl=[]
        node_y_kl=[]
        node_main_x=[]
        node_main_y=[]
        node_main_text=[]
        node_text_kl=[]
        for i in range(len(sources)):
            xx, yy = val_list[key_list.index(sources[i])]
            xx2, yy2 = val_list[key_list.index(sinks[i])]
            node_x_kl.append(xx+0.05)
            node_x_kl.append(xx2+0.05)
            node_text_kl.append(f"<b>Source {str(i+1)}</b>") 
            node_y_kl.append(yy+0.05)
            node_y_kl.append(yy2+0.05)
            node_text_kl.append(f"<b>Sink {str(i+1)}</b>")
        for i in range(0,9):
            xx, yy = val_list[key_list.index(i)]
            node_main_x.append(xx)
            node_main_y.append(yy)
            node_main_text.append(f"<b>{str(i)}</b>") 
        #xx, yy = val_list[key_list.index(11)]
        #node_main_x.append(xx)
        #node_main_y.append(yy)
        #node_main_text.append(f"<b>{str(11)}</b>") 
        #xx, yy = val_list[key_list.index(18)]
        #node_main_x.append(xx)
        #node_main_y.append(yy)
        #node_main_text.append(f"<b>{str(18)}</b>") 
        #xx, yy = val_list[key_list.index(24)]
        #node_main_x.append(xx)
        #node_main_y.append(yy)
        #node_main_text.append(f"<b>{str(24)}</b>") 
        #xx, yy = val_list[key_list.index(35)]
        #node_main_x.append(xx)
        #node_main_y.append(yy)
        #node_main_text.append(f"<b>{str(35)}</b>") 
        #xx, yy = val_list[key_list.index(56)]
        #node_main_x.append(xx)
        #node_main_y.append(yy)
        #node_main_text.append(f"<b>{str(56)}</b>") 

        for node in H2.nodes():
            xx, yy = val_list[key_list.index(node)]
            node_x.append(xx)
            node_y.append(yy)
            if node in disr_nodes_set and wv_sol[t,node]==1:
                color_map2.append('orange')
            else:
                color_map2.append(get_color(H2.nodes[node]['community']))
            if node in disr_nodes and wv_sol[t,disr_nodes.index(node)]==1:
                color_map.append('orange')
                if H2.nodes[node]['nodeType'] == 'regional':
                    size_map.append(15)
                else:
                    size_map.append(10)
            elif H2.nodes[node]['nodeType'] == 'super':
                color_map.append('steelblue')
                size_map.append(10)
            elif H2.nodes[node]['nodeType'] == 'regional':
                color_map.append('lightskyblue')
                size_map.append(15)
            elif H2.nodes[node]['nodeType'] == 'metro':
                color_map.append('mediumpurple')
                size_map.append(10)
            else: 
                color_map.append('purple')
                size_map.append(7)

        node_text = []
        for node in H2.nodes:
            node_text.append(str(node))



        #node_trace.text = node_text
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            textfont_size=14,
            hoverinfo='none',
            #text=node_text,
            marker=dict(
                opacity=1,
                showscale=False,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                #colorscale='YlGnBu',
                #reversescale=True,
                color=color_map,
                #color=node_color2,
                size=size_map,
                line_width=2,
                line_color='grey'),
                xaxis='x2', yaxis='y2')

        node_trace_kl = go.Scatter(
            x=node_x_kl, y=node_y_kl,
            mode='markers+text',
            textfont_size=10,
            textfont_color='mediumseagreen',
            hoverinfo='none',
            text=node_text_kl,
            textposition="middle center",
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')

        node_trace_main = go.Scatter(
            x=node_main_x, y=node_main_y,
            mode='markers+text',
            textfont_size=12,
            textfont_color='black',
            hoverinfo='none',
            text=node_main_text,
            textposition='middle center',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')



        node_trace_middle_kl_0 = go.Scatter(
            x=middle_x[0], y=middle_y[0],
            mode='markers',
            textfont_size=14,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')
        node_trace_middle_kl_0.text=edge_labels[0]

        node_trace_middle_kl_1 = go.Scatter(
            x=middle_x[1], y=middle_y[1],
            mode='markers',
            textfont_size=14,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')
        node_trace_middle_kl_1.text=edge_labels[1]

        node_trace_middle_kl_2 = go.Scatter(
            x=middle_x[2], y=middle_y[2],
            mode='markers',
            textfont_size=14,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')
        node_trace_middle_kl_2.text=edge_labels[2]

        node_trace_middle_kl_3 = go.Scatter(
            x=middle_x[3], y=middle_y[3],
            mode='markers',
            textfont_size=14,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')
        node_trace_middle_kl_3.text=edge_labels[3]

        node_trace_middle_kl_4 = go.Scatter(
            x=middle_x[4], y=middle_y[4],
            mode='markers',
            textfont_size=14,
            hoverinfo='text',
            marker=dict(
                showscale=False,
                opacity=0,
                size=40,
                line_width=2),
                xaxis='x2', yaxis='y2')
        node_trace_middle_kl_4.text=edge_labels[4]

        frame["data"].append(edge_trace_1)
        frame["data"].append(edge_trace_3)
        #frame["data"].append(node_trace)
        #frame["data"].append(node_trace_kl)
        #frame["data"].append(node_trace_main)
        frame["data"].append(edge_trace_2_kl_0)
        frame["data"].append(node_trace_middle_kl_0)
        frame["data"].append(edge_trace_2_kl_1)
        frame["data"].append(node_trace_middle_kl_1)
        frame["data"].append(edge_trace_2_kl_2)
        frame["data"].append(node_trace_middle_kl_2)
        frame["data"].append(edge_trace_2_kl_3)
        frame["data"].append(node_trace_middle_kl_3)
        frame["data"].append(edge_trace_2_kl_4)
        frame["data"].append(node_trace_middle_kl_4)
        frame["data"].append(node_trace)
        frame["data"].append(node_trace_kl)
        frame["data"].append(node_trace_main)
    
        

    
                    
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [t],
            {"frame": {"duration": 0, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 0}}
        ],
            "label": str(t),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    table3=go.Table(columnwidth=[0.5, 0.5 , 1.5, 0.5],header=dict(values=['Time','(Source, Sink)', 'Route','Flow']),
                cells=dict(values=[[table3_t[i] for i in range(len(table3_t))], [table3_kl[i] for i in range(len(table3_t))], [table3_routes[i] for i in range(len(table3_t))], [table3_flow[i] for i in range(len(table3_t))]],font=dict(color='black', size=9)),domain=dict(x=[0.6, 1],
                    y=[0, 0.35]))

    fig_dict["data"].append(table3)   

    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig_dict["layout"]["paper_bgcolor"] = "white"
    fig_dict["layout"]["plot_bgcolor"] = "white"

    fig_dict["layout"]["annotations"]= [
            go.layout.Annotation(
                showarrow=False,
                text='<b>Predictive maintenance plan for nodes:</b>',
                font=dict(
                    color="black",
                    size=14
                ),
                xref='paper',
                yref='paper',
                xanchor='right',
                x=1,
                yanchor='top',
                y=1
            )]

    fig = go.Figure(fig_dict)
    fig.add_annotation(x=1, y=0.7,
                text='<b>Predictive maintenance plan for arcs:   </b>',
                font=dict(
                    color="black",
                    size=14
                ),
                showarrow=False,
                xref='paper',
                yref='paper',
                xanchor='right',
                yanchor='top')
    fig.add_annotation(x=1, y=0.4,
                text='<b>Routes for traffic:                               </b>',
                font=dict(
                    color="black",
                    size=14
                ),
                showarrow=False,
                xref='paper',
                yref='paper',
                xanchor='right',
                yanchor='top')


    fig.show()
