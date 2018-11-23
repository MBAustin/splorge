import networkx as nx
import plotly.offline
import plotly.graph_objs as go

def createDiGraph():
    # Create a directed graph (digraph) object; i.e., a graph in which the edges
    # have a direction associated with them.
    G = nx.DiGraph()

    # Add nodes:
    nodes = ['A', 'B', 'C', 'D', 'E']
    G.add_nodes_from(nodes)

    # Add edges or links between the nodes:
    edges = [('A','B'), ('B','C'), ('B', 'D'), ('D', 'E')]
    G.add_edges_from(edges)
    return G

g = createDiGraph()

# Get a layout for the nodes according to some algorithm.
# See https://networkx.github.io/documentation/stable/reference/drawing.html#layout
# for alternative algorithms that are available.
# Set random_state (default=None) if you want the layout to be deterministic
# and repeatable.
node_positions = nx.spring_layout(g)

myX = [1,2,3,2.5,3.5]
myY = [4,5,4,3,3]

# The nodes will be plotted as a scatter plot of markers with their names
# above each circle:
node_trace = go.Scatter(
    x=myX,
    y=myY,
    text=['test1', 'test2', 'test3'],
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
            color='rgb(200,0,0)',
            size=25,
            line=go.Line(width=1, color='rgb(0,0,0)')))

# for node in node_positions:
#     x, y = node_positions[node]
#     node_trace['x'].append(x)
#     node_trace['y'].append(y)
#     node_trace['text'].append(node)

# The edges will be drawn as lines:
edge_trace = go.Scatter(
    x=myX,
    y=myY,
    line=go.Line(width=1, color='rgb(150,150,150)'),
    hoverinfo='none',
    mode='lines')

# for edge in g.edges:
#     x0, y0 = node_positions[edge[0]]
#     x1, y1 = node_positions[edge[1]]
#     edge_trace['x'].extend([x0, x1, None])
#     edge_trace['y'].extend([y0, y1, None])

# Create figure:
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
