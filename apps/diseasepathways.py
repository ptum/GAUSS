'''
Created on Apr 10, 2018

@author: schoobdar
'''
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from dash.dependencies import Input, Output
from gauss.apps.app_config import *
import os
import json

d= 12
x=df.iloc[d,[5,3,1]].tolist()
selected_m = sig_modules[x[0]][x[1]][x[2]]
# sg2 = graph_list[x[1]].subgraph(selected_m)
sg2 = G3.subgraph(selected_m)
FIGURE= plot_net(sg2, 'gs_name', 2)



layout =  html.Div([  # page 6

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
                html.P("SELECT a phenotype in the dropdown to add it to table below."),
                dcc.Dropdown(id='trait_group',
                        multi=True,
                        value=[ '' ],
                        options=[{'label': i, 'value': i} for i in sorted(df['trait.simplified'].unique().tolist())]),
            ], className="row"),
            # Row 2
            html.Div([

                html.Div([
                    html.H6(["List of disease associated modules"], className="gs-header gs-text-header padded"),
                    dt.DataTable(
                       rows=filter_data(['Schizophrenia',]).to_dict('records'),
                       # optional - sets the order of columns    
                       row_selectable=True,
                       filterable=True,
                       sortable=True,
                       selected_row_indices=[],
                       id='datatable-traitModule'
                         ),
#                     html.Table(make_dash_table(filter_data(['Schizophrenia',]).iloc[:,:10]),id='datatable-traitModule' ),
                ], className=" twelve columns"),

            ], className="row "),
               # Row 3
            html.Div([

                html.Div([
                    html.H6(["Selected module graph"], className="gs-header gs-text-header padded"),
                    dcc.Graph(
                            id='graph-traitModule',
                            figure= FIGURE,),

                    ], className=" six columns"),
                html.Div([
                    html.H6(["Annotated terms"],
                            className="gs-header gs-text-header padded"),
                    html.Table(id='datatable-annotationTerms')
                    ], className="six columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

@app.callback(
    Output(component_id='datatable-traitModule', component_property='rows'),
    [Input(component_id='trait_group', component_property='value'),]
         )
def update_table(categories):
    import numpy as np
    np.set_printoptions(precision=10)
    sub_res = filter_data(categories)
#     sub_res['Pvalue'] = sub_res['Pvalue'].apply(format_e)
    sub_res['-log(p)'] = sub_res.Pvalue.apply(lambda x:round(-1*np.log10(x),1))
    return sub_res.to_dict('records')

@app.callback(
    Output('graph-traitModule', 'figure'),
    [Input('datatable-traitModule', 'rows'),
     Input('datatable-traitModule', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    res =  rows[selected_row_indices[0]]
    pval = ''#res['pvalue']
    mm = sig_modules[res['teamName']][res['Network']][res['Module ID']]
#     sg= graph_list[ind[1]].subgraph(selected_m)
    sgg = G3.subgraph(mm)
    return plot_net(sgg,res['Network'],pval)

@app.callback(
    Output('datatable-annotationTerms', 'children'),
    [Input('datatable-traitModule', 'rows'),
     Input('datatable-traitModule', 'selected_row_indices')])
def update_anno_table(rows, selected_row_indices):
    res =  rows[selected_row_indices[0]]
    ind =[str(res['teamName']),str(res['Network']),int(res['Module ID'])]
    return make_dash_table(filter_annotation(ind))


    
