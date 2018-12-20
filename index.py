import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output,State
import os
from apps.app_config import app
from apps import overview,diseasepathways,enrichmentanalysis, contacts, pascalanalysis


noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])
 
# 
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname =='/' or pathname == '/overview':
        return overview.layout
    elif pathname == '/disease-pathways':
        return  diseasepathways.layout
    elif pathname == '/enrichment-analysis':
        return  enrichmentanalysis.layout
    elif pathname == '/pathway-analysis':
        return  pascalanalysis.layout
    elif pathname == '/about':
        return  contacts.layout
    else:
        return noPage

# app.layout = diseasepathways.layout

external_css = [
                "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/sarvi/pen/ZxPEgR.css",
#                 "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]


for css in external_css:
    app.css.append_css({"external_url": css})
# external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#                 "//fonts.googleapis.com/css?family=Raleway:400,300,600",
#                 "//fonts.googleapis.com/css?family=Dosis:Medium",
#                 "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]
# 
# 
# for css in external_css:
#     app.css.append_css({"external_url": css})

server = app.server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run_server(debug=True, host='localhost', port=port)
