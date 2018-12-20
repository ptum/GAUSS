'''
Created on Apr 10, 2018

@author: schoobdar
'''
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import numpy as np
from dash.dependencies import Input, Output,State
from gauss.apps.app_config import *

def jaccard_overlap(m1,m2):
    return 1.* len(set(m1).intersection(m2))/len(set(m1).union(m2))

# total number of genes 
def find_enriched_module(selected_m):
    M =len(set(all_genes))
    from scipy.stats import hypergeom
    N = len(selected_m) # sample size
    overlap_profile=[]
    for m,i  in sig_modules.items():
        for n,j in i.items():
            for l,k in list(j.items()):
                d= jaccard_overlap(k,selected_m)
                l_intersect = len(set(selected_m).intersection(k))
                l_n= len(k)
                if d>0:
                    pval = hypergeom.sf(l_intersect-1, M, l_n, N)
                    overlap_profile.append([m,n,l,l_intersect,d,pval])
    #df_subset = df.loc[(df['teamName'].isin(selection)) & (df['net']=='3_signal')].sort_values(['pval','module_size']).reset_index()
    #df_subset.iloc[:,[7,4,6,2,5,3,1]].rename(columns={'mid':'Module ID','module_size':'Module Size','pval':'Pvalue','gwas_name':'GWAS             
    mp = pd.DataFrame(overlap_profile)
    mp.columns=['teamName','network','mid','intersection','Jaccard','pvalue']
    res = mp[mp.pvalue*mp.shape[0]<0.05]
    res['-log(p)'] = res.pvalue.apply(lambda x:round(-1*np.log10(x),1))
    merged_res = pd.merge(res,df,how='left',left_on=['teamName','network','mid'],right_on=['teamName','net','mid'])
    res_out = merged_res.iloc[:,[1,6,8,14]].sort_values('-log(p)',ascending=False)
    res_out.columns= [ 'Phenotype','Network','-Log(pvalue)','Module Size']
    return res_out
 


layout = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1
            html.Div([
                html.H6('Disease Module Enrichment Analysis',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("Enter a list of gene symboles, comma seperated and press submit."),
                dcc.Input(id='input-box', type='text'),
                html.Button('Submit', id='button'),
                dcc.Checklist(options=[{'label': 'Sample1', 'value': 's1'},{'label': 'Sample2', 'value': 's2'}], values=['s2'], labelStyle={'display': 'inline-block'},id='sample-item'),
            ], className="row"),
            # Row 2
            html.Div([
                html.H6('List of disease modules that the input gene list is enriched in.',
                        className="gs-header gs-text-header padded"),
                html.Div(id='output-container-button',
                         ),
                html.Br([]),
                html.P("Select a module from list to visualize it."),
                dt.DataTable(
                      rows=[{}],
                      # optional - sets the order of columns    
                      row_selectable=True,
                      filterable=True,
                      sortable=True,
                      selected_row_indices=[],
                      columns=  [ ' Phenotype','Network','-Log(pvalue)','Module Size'],
                      id='datatable-enrichedModules'
                        )
            ], className="row "),
            # Row 3
            html.Div([

                html.Div([
                    html.H6(["Selected module graph"], className="gs-header gs-text-header padded"),
                    dcc.Graph(
                            id='graph-traitModule-en',
                            ),
                    ], className=" six columns"),
                html.Div([
                    html.H6(["Annotated terms"],
                            className="gs-header gs-text-header padded"),
                    html.Table(id='datatable-annotationTerms-en')
                    ], className="six columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")



@app.callback(
    Output('datatable-enrichedModules', 'rows'),
    [Input('button', 'n_clicks'),
     Input('sample-item','values')],
    [State('input-box', 'value')])
def update_enriched_modules(n_clicks, sample_value,input_value):
    import re
    if 's1' in sample_value:
        query_set=['HIST2H2BD',  'HIST1H2BL',  'HIST2H2BC',  'HIST3H2BB',  'HIST2H2BE',  'HIST2H2BF',  'HIST1H2BK',  'HIST1H2BO',  'HIST1H2BH',  'HIST1H2BN']
    elif 's2' in sample_value:
        query_set= ['TJP2',  'RPL5',  'SUPT20H']
    else :
        query_set = [x for x in [re.sub('[^A-Za-z0-9]+', '',str(x)).upper() for x in input_value.split(',')] if x!='' and x is not None]
    return find_enriched_module(query_set).to_dict('records')


@app.callback(
    Output('graph-traitModule-en', 'figure'),
    [Input('datatable-enrichedModules', 'rows'),
     Input('datatable-enrichedModules', 'selected_row_indices')
     ])
def update_figure_enrichment(rows, selected_row_indices):
    res =  rows[selected_row_indices[0]]
      
    mm = sig_modules[res['teamName']][res['network']][res['mid']]
#     sg= graph_list[ind[1]].subgraph(selected_m)
    pval = ''#res['pvalue']
    sgg = G3.subgraph(mm)
    return plot_net(sgg,res['network'],pval)

# @app.callback(
#     Output('datatable-annotationTerms-en', 'children'),
#     [Input('datatable-enrichedModules', 'rows'),
#      Input('datatable-enrichedModules', 'selected_row_indices')])
# def update_anno_table_en(rows, selected_row_indices):
#     res =  rows[selected_row_indices[0]]
#     ind =[str(res['teamName']),str(res['network']),int(res['mid'])]
#     return make_dash_table(filter_annotation(ind))

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks'),
     Input('sample-item','values')],
    [State('input-box', 'value')])
def update_output(n_clicks, sample_value,input_value):
    if 's1'  in sample_value:
        return 'The input gene list is \n\n"{}" '.format(['HIST2H2BD',  'HIST1H2BL',  'HIST2H2BC',  'HIST3H2BB',  'HIST2H2BE',  'HIST2H2BF',  'HIST1H2BK',  'HIST1H2BO',  'HIST1H2BH',  'HIST1H2BN'])
    if 's2'  in sample_value:
        return 'The input gene list is \n\n"{}" '.format(['TJP2',  'RPL5',  'SUPT20H'])
    if input_value is not None :
        return 'The input gene list is \n"{}" '.format(input_value)
    
    
