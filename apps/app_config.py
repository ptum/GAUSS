import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import pandas as pd
from plotly import graph_objs as go
import csv
import numpy as np
import flask
import os
######### Start app

app = dash.Dash(name='GAUSS')
app.config.suppress_callback_exceptions = True

######### LOADING DATA
path_to_data = '/var/www/FlaskApp/data/'
BACKGROUND = 'rgb(230, 230, 230)'




def plot_net(g,gs_name,pval):
    pos=nx.fruchterman_reingold_layout(g)
    N = nx.number_of_nodes(g)
    labels = [str(u[0]) for u in g.nodes(data=True)]
    # d = g.degree().values()
    node_color =[i[1] for i in g.degree()]
    hover_text = ["%s <br> "%i for i in labels]
    Xv=[pos[k][0] for k in g.nodes()]
    Yv=[pos[k][1] for k in g.nodes()]
    Xed=[]
    Yed=[]
    for edge in nx.edges(g):
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None] 
    ### plotting setting
        trace1=dict(
                type='scatter',
                x=Xed,
                y=Yed,
                mode='lines',
                line=dict(color='rgb(210,210,210)', width=1),
#                    hoverinfo='none'
                )

    trace2=dict(
                type='scatter',
                x=Xv,
                y=Yv,
                mode='markers',
                name='net',
                marker=dict(symbol='dot',
                             size=20, 
                             color=node_color,
                             colorscale='Viridis',
                             showscale=True,
                             colorbar = dict(
                                        title = 'Gene association, -log(pvalue)',
                                        titleside = 'top',
                                        tickmode = 'array',
                                        ticks = 'outside'
                                    ),
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
                )

    layout=dict(
                title='',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=40,l=5,r=5,t=40),
                annotations=[ dict(
                    text='',
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=350  )

    data1=[trace1, trace2]
    fig1=dict(data=data1, layout=layout)
    return fig1


def trait_sim_graph():
    g = nx.read_graphml(path_to_data+'trait_net_gephi_layout.graphml')
    Xv=[]
    Yv=[]
    node_size=[]
    labels=[]
    node_color=[]
    for u,node in g.nodes(data=True):
        if g.degree(u)!=0:
            Xv.append(node['x'])
            Yv.append(node['y'])
            node_size.append(node['size'])
            labels.append(node['name'])
            node_color.append('rgb('+','.join(map(str,[node['r'],node['g'],node['b']]))+')')

    Xed=[]
    Yed=[]
    for edge in nx.edges(g):
        Xed+=[g.node[edge[0]]['x'],g.node[edge[1]]['x'], None]
        Yed+=[g.node[edge[0]]['y'],g.node[edge[1]]['y'], None]
    trace1=dict(
                type='scatter',
                x=Xed,
                y=Yed,
                mode='lines',
                line=dict(color='rgb(210,210,210)', width=1),
#                    hoverinfo='none'
                )

    trace2=dict(
                type='scatter',
                x=Xv,
                y=Yv,
                mode='markers',
                name='net',
                marker=dict(symbol='dot',
                             size=node_size, 
                             color=node_color,
                             colorscale=node_color,
                             showscale=False,
                             colorbar = dict(
                                        title = 'Number of modules',
                                        titleside = 'top',
                                        tickmode = 'array',
                                        ticks = 'outside'
                                    ),
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
                )

    layout=dict(
                title='<br>Network of Phenotypes',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=40,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Source: <a href='https://www.biorxiv.org/content/early/2018/02/15/265553'> Open Community Challenge Reveals Molecular Network Modules with Key Roles in Diseases</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                width= 700,
                height=700)

    data1=[trace1, trace2]
    fig1=dict(data=data1, layout=layout)
    return fig1

###### LOADING DATA

df =pd.read_csv(path_to_data+'SC1_sig_disease_modules_with_consensus_new_gwas_cat_04042018.txt')
annotations = pd.read_csv(path_to_data+'annotationEnrichment_terms_sig_modules_05042018.txt',low_memory=False)

# graph_list= {}
# for f in os.listdir(path_to_data+'/networks/'):
#     if f.endswith('.txt'):
#         net= '_'.join(f.split('_')[:2])
#         g= nx.read_edgelist(path_to_data+'/networks/'+f,delimiter='\t',data=(('weight',float),))
#         graph_list[net] = g

G3= nx.read_edgelist(path_to_data+'networks/3_signal_omnipath_directed.txt',delimiter='\t',data=(('weight',float),))

L = csv.reader(open(path_to_data+'SC1_sig_modules_with_consensus_23102017.txt','rU'),delimiter='\t')
sig_modules= {}
all_genes =[]
for r in L:
    teamName=r[1]
    if teamName not in sig_modules:
        sig_modules[teamName]={}
    if r[2] not in sig_modules[teamName]:
        sig_modules[teamName][r[2]]={}
    sig_modules[teamName][r[2]][int(r[3])]=r[4:]
    all_genes+=r[4:]


######### functions

def get_logo():
    import base64
    image_filename = path_to_data+ 'banner_vis.jpg' # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    logo = html.Div([

        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), height='150', width='1000')
        ], className="ten columns padded"),

        

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Disease Modules')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/overview', className="tab first"),

        dcc.Link('Disease Modules   ', href='/disease-pathways', className="tab"),

        dcc.Link('Enrichment Analysis   ', href='/enrichment-analysis', className="tab"),

        dcc.Link('Pathway scoring Analysis   ', href='/pathway-analysis', className="tab"),
        
        dcc.Link('About   ', href='/about', className="tab")

        

    ], className="row ")
    return menu

def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def filter_data(selection):
    df_subset = df.loc[(df['trait.simplified'].isin(selection)) & (df['net']=='3_signal')].sort_values(['pval','module_size']).reset_index()
    return df_subset.iloc[:,[7,4,6,2,5,3,1]].rename(columns={'mid':'Module ID','module_size':'Module Size','pval':'Pvalue','gwas_name':'GWAS name','net':'Network','traitGroup':'Phenotype category'})
def filter_annotation(x):
    res = annotations[(annotations['teamName']==x[0])  & (annotations['net']==x[1]) & (annotations['mid']==x[2])].iloc[:,[2,5]]
    return res.rename({'pathwayDb':'Annotation DB','term':'Term'}).head()

