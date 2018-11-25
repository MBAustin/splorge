import networkx as nx
import plotly.offline
import plotly.graph_objs as go
import json


name_list = []
start_size = 100
depth_list = []
color_list = ['rgb(200,0,0)', 'rgb(0,200,0)', 'rgb(0,0,200)', 'rgb(200,200,0)', 'rgb(200,0,200)',
              'rgb(0,200,200)', ]

def create_digraph(filename):

    with open(filename) as log:
        node_data = json.load(log)

    # Create a directed graph (digraph) object; i.e., a graph in which the edges
    # have a direction associated with them.
    G = nx.DiGraph()

    # Add nodes:
    node_list = []
    edge_list = []
    parse_nodes(node_data, node_list, edge_list, name_list, 1)
    G.add_nodes_from(node_list)

    # Add edges or links between the nodes:
    G.add_edges_from(edge_list)
    return G


def parse_nodes(node_data, node_list, edge_list, name_list, depth):
    node_name = list(node_data.keys())[0]
    name_list.append(node_name)
    depth_list.append(depth)
    node = (node_name, node_data[node_name]['time'])
    node_list.append(node)
    for child in node_data[node_name]['children']:
        child_node = parse_nodes(child, node_list, edge_list, name_list, depth+1)
        edge_list.append((node, child_node))
    return node


g = create_digraph('test_data2.json')

node_positions = nx.spring_layout(g)

node_trace = go.Scatter(
    x=[pos[0] for pos in node_positions.values()],
    y=[pos[1] for pos in node_positions.values()],
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
            size=[(start_size * 1/(depth)) for depth in depth_list],
            line=go.Line(width=1, color='rgb(0,0,0)')))


print("Name list: " + str(name_list))
edgesX = []
edgesY = []
for edge in g.edges:
    x0, y0 = node_positions[edge[0]]
    x1, y1 = node_positions[edge[1]]
    edgesX.extend([x0, x1, None])
    edgesY.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edgesX,
    y=edgesY,
    line=go.Line(width=1, color='rgb(150,150,150)'),
    hoverinfo='none',
    mode='lines')


fig = go.Figure(data = go.Data([edge_trace, node_trace]),
             layout = go.Layout(
                title = 'Sample Network',
                titlefont = dict(size=16),
                showlegend = False,
                hovermode = 'closest',
                margin = dict(b=20,l=20,r=20,t=40),
                xaxis = go.XAxis(showgrid=False, zeroline=False, showticklabels=True),
                yaxis = go.YAxis(showgrid=False, zeroline=False, showticklabels=True)))

plotly.offline.plot(fig)
