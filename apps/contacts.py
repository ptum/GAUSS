'''
Created on Apr 10, 2018

@author: schoobdar
'''

import dash_core_components as dcc
import dash_html_components as html
from apps.app_config import *
layout = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1
            html.Div([
                html.H6('About',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P(children=["A web app and library for visualising disease associated modules from ",
                            html.A(
                                children='DREAM challenge for disease modules identification',
                                target= '_blank',
                                href='https://www.synapse.org/#!Synapse:syn6156761/wiki/'),'.'])
                            
            ], className="row"),
            # Row 2
            html.Div([
                html.H6('Contact information:',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("If you have questions, comments or suggestions, we'd like to hear them:"),
                html.P('@Sarvenaz Choobdar (firstname.lastname@unil.ch)'),
            ], className="row"),
            # Row 3
            html.Div([
                html.H6('Cite:',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("Challenge preprint:",style = {'fontWeight':600}),
                html.P(children =["- Open Community Challenge Reveals Molecular Network Modules with Key Roles in Diseases",
                                    html.Br([]),"Sarvenaz Choobdar, Mehmet E. Ahsen, Jake Crawford, Mattia Tomasoni, David Lamparter, \
                                        Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, \
                                        The DREAM Module Identification Challenge Consortium, Aravind Subramanian, \
                                        Gustavo Stolovitzky, Zoltan Kutalik, Kasper Lage, Donna K. Slonim, Julio Saez-Rodriguez, \
                                        Lenore J. Cowen, Sven Bergmann, Daniel Marbach.",html.Br([]),
                                 html.A(children ='bioRxiv 265553 (2018).', target='_blank', href='https://www.biorxiv.org/content/early/2018/02/15/265553')
                        ]),
            ], className="row"),

        ], className="subpage")

    ], className="page")
