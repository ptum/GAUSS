import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
from apps.app_config import *

FIGURE=trait_sim_graph()

sub_df =df.groupby(['trait.simplified','net'])['mid'].count().reset_index()

def fetch_trait_name( hoverData ):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                trait_name = str(FIGURE['data'][0]['text'][point_number]).strip()
                return trait_name
    return None


def fetch_module_count(res):
    m_labels = sub_df[sub_df['trait.simplified']==res]['net']
    m_values = sub_df[sub_df['trait.simplified']==res]['mid']
    return m_labels,m_values
def fetch_term_count(res):
    module_list = df.loc[(df['trait.simplified'].isin([res,])) & (df['net']=='3_signal')].sort_values(['pval','module_size']).loc[:,['teamName','net','mid']].values
    x,y,z  =  module_list.transpose()
    anno_sub =  annotations[(annotations['teamName'].isin(x))  & (annotations['net'].isin(y)) & (annotations['mid'].isin(z))].groupby('pathwayDb')['term'].count().reset_index()
    ano_labels = anno_sub['pathwayDb']
    ano_values = anno_sub['term']
    return ano_labels,ano_values

def make_pie_chart(labels,values,title,name):
    fig = {
      "data": [
        {
          "values": values,
          "labels": labels,
          "name": "Number of Modules",
          "hoverinfo":"label+value",
          "hole": .4,
          "type": "pie"
        },     
        ],
      "layout": {
            "title":title,
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": name,
                    
                },
              
            ],
            'legend': dict(orientation='h')
        }
    }


    return fig
t_name = 'Cross-disorder'
ml,mv = fetch_module_count(t_name)
PIE_net_FIGURE =make_pie_chart(ml,mv,'Number of Modules','Networks')
al,av= fetch_term_count(t_name)
PIE_terms_FIGURE =make_pie_chart(al,av,'Number of Terms','Terms')
layout = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1
            html.Div([
                html.H6('Description',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
               
                html.P(['''
                        This is platform to browse and visualize the results of ''',
                        html.A(
                            children='DREAM challenge for disease modules identification',
                            target= '_blank',
                            href='https://www.synapse.org/#!Synapse:syn6156761/wiki/',
                            
                        ),
                        ' an open competition to comprehensively assess module identification methods across diverse gene, \
                        protein and signaling networks. Predicted network modules,association with complex traits and diseases are visualized through this platform.'
                    ])
                       
                       
            ], className="row"),
            # Row 2
            html.Div([
                html.Div([
                html.H6('Disease Modules Network',
                          className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P('HOVER over nodes in the graph below to see the information about pathways related to the selected phenotype.'),
                dcc.Graph(
                    id='graph-phenotype_network',
                    style=dict(width='700px'),
                    hoverData=dict( points=[dict(pointNumber=0)] ),
                    figure= FIGURE
                ),
                ], className='eight columns',style=dict(textAlign='center')),
                html.Div([
                html.H6('Module informations',
                          className="gs-header gs-text-header padded"),
                html.Br([]),
                html.Div([
                          dcc.Graph(
                                    id='graph-phenotype-pie1', figure=PIE_net_FIGURE)
                          ],className='row'),
                dcc.Graph(
                id='graph-phenotype_pie2',
                figure= PIE_terms_FIGURE
                ), 
                ], className='four columns',style=dict(textAlign='center'))  
            ], className="row "),

        ], className="subpage")

    ], className="page")


@app.callback(
    Output('graph-phenotype-pie1', 'figure'),
    [Input('graph-phenotype_network', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)



