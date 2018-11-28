import networkx as nx
import plotly.offline
import plotly.graph_objs as go
import json

import warnings
warnings.filterwarnings("ignore")



filename = 'logger/PythonShootGameOut.json'
with open(filename) as log_json:
    data_dict = json.load(log_json)

start_size = 90
node_lists = [[]]
edge_lists = [[]]
current_node_list = []
current_edge_list = []
name_list = []
depth_list = []
size_list = []
maxX = []
maxY = []
minX = []
minY = []
color_list = ['rgb(200,0,0)', 'rgb(200,200,0)', 'rgb(200,0,200)', 'rgb(0,200,0)', 'rgb(0,200,200)',
              'rgb(100,0,0)', 'rgb(100,100,0)', 'rgb(100,0,100)', 'rgb(0,100,0)', 'rgb(0,100,100)',
              'rgb(50,60,70)', 'rgb(80,70,60)', 'rgb(255,150,100)', 'rgb(100,150,255)', 'rgb(150,255,100)']

def parse_nodes(node_data, depth):
    depth_list.append(depth)
    node = (node_data['name'], node_data['time'])
    time_span = 0
    if current_node_list:
        start_time = current_node_list[-1][1]
        time_span = int(node_data['time']) - int(start_time)

    size_list.append(time_span + 30)
    if time_span > 0:
        # name_list.append(node_data['name'] + ': ' + str(time_span) + ' ms')
        name_list.append(node_data['name'])
    else:
        name_list.append(node_data['name'])
    current_node_list.append(node)
    node_lists.append(current_node_list.copy())
    edge_lists.append(current_edge_list.copy())
    for child in node_data['children']:
        current_edge_list.append((node, (child['name'], child['time'])))
        parse_nodes(child, depth+1)

    return node

parse_nodes(data_dict,1)

def create_digraph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G



def build_data(digraph):
    if digraph.nodes():
        first_node = list(digraph.nodes)[0]
        node_pos = nx.spring_layout(digraph, pos={first_node:(0,0)}, fixed=[first_node], seed=1)
        maxX.append(max([pos[0] for pos in node_pos.values()]))
        maxY.append(max([pos[1] for pos in node_pos.values()]))
        minX.append(min([pos[1] for pos in node_pos.values()]))
        minY.append(min([pos[1] for pos in node_pos.values()]))
    else:
        node_pos = nx.spring_layout(digraph, seed=1)



    node_trace = go.Scatter(
        x=[pos[0] for pos in node_pos.values()],
        y=[pos[1] for pos in node_pos.values()],
        text=name_list,
        mode='markers+text',
        textposition='top center',
        textfont=dict(
            family='arial',
            size=18,
            color='rgb(0,0,0)'
        ),
        hoverinfo='none',
        marker=go.Marker(
                showscale=False,
                color=[color_list[depth-1 % len(color_list)] for depth in depth_list],
                opacity=1,
                #size= [(start_size * 1/(depth)) for depth in depth_list],
                size= size_list,
                line=go.Line(width=1, color='rgb(0,0,0)')))

    edgesX = []
    edgesY = []
    for edge in digraph.edges:
        try:
            x0, y0 = node_pos[edge[0]]
            x1, y1 = node_pos[edge[1]]
            edgesX.extend([x0, x1, None])
            edgesY.extend([y0, y1, None])
        except KeyError:
            continue

    edge_trace = go.Scatter(
        x=edgesX,
        y=edgesY,
        line=go.Line(width=1, color='rgb(150,150,150)'),
        hoverinfo='none',
        mode='lines')

    return go.Data([edge_trace, node_trace])




data_graph = create_digraph(current_node_list, current_edge_list)
data_vals = build_data(data_graph)

frame_list = []
for i in range(len(node_lists)):
    node_list = node_lists[i]
    edge_list = edge_lists[i]
    frame_graph = create_digraph(node_list, edge_list)
    frame_data = build_data(frame_graph)
    frame_list.append({'data':frame_data, 'name':'frame{}'.format(i)})

trueMaxX = max(maxX) + 0.3
trueMaxY = max(maxY) + 0.3
trueMinX = min(minX) - 0.3
trueMinY = min(minY) - 0.3

fig = go.Figure(data = data_vals,
             layout = go.Layout(
                title = '{}: Dynamic Call Graph'.format(filename),
                titlefont = dict(size=16),
                updatemenus = [{'type': 'buttons',
                                      'buttons': [{'label': 'Play',
                                                   'method': 'animate',
                                                   'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}]}]}],
                showlegend = False,
                hovermode = 'closest',
                margin = dict(b=20,l=20,r=20,t=40),
                xaxis = go.XAxis(range=[-1*trueMaxX, trueMaxX], showgrid=False, zeroline=False, showticklabels=False),
                yaxis = go.YAxis(range=[-1*trueMaxY, trueMaxY], showgrid=False, zeroline=False, showticklabels=False)),
                frames=frame_list)

plotly.offline.plot(fig)