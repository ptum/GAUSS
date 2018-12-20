'''
Created on Apr 10, 2018

@author: schoobdar
'''
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import numpy as np
from dash.dependencies import Input, Output,State
from FlaskApp.apps.app_config import *
import os,subprocess,hashlib
import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random
import re
import dns.resolver
import socket
from .pascal_functions import *

####################################
path_to_pascal_output='/var/www/FlaskApp/FlaskApp/pascal_output/'
path_to_data = '/var/www/FlaskApp/data'
path_to_submitted_geneSets = '/var/www/FlaskApp/FlaskApp/pascal_dowloaded_files/'
def verify_geneSet(gSet):
    geneIds = pd.read_csv(path_to_data+'/entrezID_symbol.txt',sep=',')
    unique_geneSymbols = set(geneIds.iloc[:,1].unique())
    if len(unique_geneSymbols.intersection(gSet))>=3 :
        return True
    else:
        return False
def send_email(toaddr,attachment_file,has_attachemet=False):
    fromaddr = "gauss.cbg@gmail.com"
#     fromaddr = 'sarvenaz.choobdar@unil.ch'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "GAUSS: Genome-wide Pathway Scoring"
     
    body = "Hello! \nThis is GAUSS, a web application for Pathway scoring using Genome-wide association studies. \nWe will get back to you with the results ASAP. \n Best \nGAUSS " # The /n separates the message from the headers
    msg.attach(MIMEText(body, 'plain'))
    if has_attachemet:
#         attachment_file = "gggg.txt"
        attachment = open("/Users/schoobdar/Documents/workspace/genesNetwork_app/"+attachment_file, "rb")
         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_file)
         
        msg.attach(part)

    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
#     mailserver = smtplib.SMTP('smtp.unil.ch', 465)
    
#     mailserver.set_debuglevel(1)

    mailserver.starttls()
    mailserver.login(fromaddr, "sarvenazmattia2018") #gmail pass

    text = msg.as_string()
    mailserver.sendmail(fromaddr, toaddr, text)
    mailserver.quit()
    
    
def verify_input_email(email_address):
#     addressToVerify = email_address
#     match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
#     
#     if match == None:
#         print(('Bad Syntax in ' + addressToVerify))
# #         raise ValueError('Bad Syntax')
#         return False
#     
#     #Step 2: Getting MX record
#     #Pull domain name from email address
#     domain_name = email_address.split('@')[1]
#     
#     #get the MX record for the domain
#     records = dns.resolver.query(domain_name, 'MX')
#     mxRecord = records[0].exchange
#     mxRecord = str(mxRecord)
#     
#     #Step 3: ping email server
#     #check if the email address exists
#     
#     # Get local server hostname
#     host = socket.gethostname()
#     
#     # SMTP lib setup (use debug level for full output)
#     mailserver = smtplib.SMTP()
#     mailserver.set_debuglevel(0)
#     
#     # SMTP Conversation
#     mailserver.connect(mxRecord,port=1025)
#     mailserver.helo(host)
#     mailserver.mail('me@domain.com')
#     code, message = mailserver.rcpt(str(addressToVerify))
#     mailserver.quit()
#     
#     # Assume 250 as Success
#     if code == 250:
#         return True
#     else:
#         return False
    return  True

def save_geneSet_to_file(q,fname):
    id_ = str(random.randint(1000,2000))#str(int(hashlib.md5(q.encode('utf-8')).hexdigest(), 16))
    saved_file_name = path_to_submitted_geneSets+fname+'_'+id_
    with open(saved_file_name,'wb') as sfile:
        sfile.write('1,'+fname+','+','.join(q))
    return saved_file_name

def send_results(submission_file,email_address):
    pascal_results_file= collect_pascal_outputs(submission_file)
    send_email(email_address, pascal_results_file)
    return

#########

layout = html.Div([  # page 6
        html.Div([
            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),
            # Row 1
            html.Div([
                html.H6('Pathway scoring analysis',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("Enter a list of gene symboles, comma seperated and press submit."),
                dcc.Input(id='input-box-geneSet', type='text',style={'width': 300,'height':300},placeholder='Enter your gene list...'),
                html.P("SELECT a phenotype in the dropdown for pathway scoring."),
                dcc.Dropdown(id='trait_group',
                        multi=True,
                        value=[ '' ],
                        options=[{'label': i, 'value': i} for i in sorted(df['trait.simplified'].unique().tolist())]),
                html.P("Enter your email address to receive the results."),
                dcc.Input(id='input-box-Email', type='text',placeholder='Enter your email address...',style={'width': 400}),                
                html.Br([]),
                html.Button('Submit', id='button'),
                html.Br([]),
              
            ], className="row"),
            # Row 2
            html.Div([
                html.Br([]),

                html.Div(id='submission-msg',className="gs-header gs-text-header padded"
                         ),
                html.Br([]),
                
            ], className="row "),
#             # Row 3
#             html.Div([
# 
#                 html.Div([
#                     html.H6(["Selected module graph"], className="gs-header gs-text-header padded"),
#                     dcc.Graph(
#                             id='graph-traitModule-en',
#                             ),
#                     ], className=" six columns"),
#                 html.Div([
#                     html.H6(["Annotated terms"],
#                             className="gs-header gs-text-header padded"),
#                     html.Table(id='datatable-annotationTerms-en')
#                     ], className="six columns"),
# 
#             ], className="row "),

        ], className="subpage")

    ], className="page")




@app.callback(
    Output('submission-msg', 'children'),
    [Input('button', 'n_clicks'),Input(component_id='trait_group', component_property='value'),],
    [State('input-box-Email', 'value'),
     State('input-box-geneSet', 'value')])
def update_output(n_clicks,selected_gwas,input_value,geneSet):
    import re
    if n_clicks>0:
        
        if verify_input_email(input_value):
            query_set = [x for x in [re.sub('[^A-Za-z0-9]+', '',str(x)).upper() for x in geneSet.split(',')] if x!='' and x is not None]
            if verify_geneSet(query_set):
                selected_gwas_files = df.loc[(df['trait.simplified'].isin(selected_gwas))]['gwas_name'].unique().tolist()
                cleaned_email = re.sub('[^A-Za-z0-9]+', '',input_value).lower()
                pascal_input_geneSet_file = save_geneSet_to_file(query_set,cleaned_email)
#                 print "Gene Set save in:", pascal_input_geneSet_file
                send_email(input_value,'',False)
                run_pascal(pascal_input_geneSet_file,selected_gwas_files)
#                 while not is_pascal_done(pascal_input_geneSet_file, selected_gwas_files):
#                     time.sleep(10)
                is_pascal_done(pascal_input_geneSet_file, selected_gwas_files)
                print("Collecting results")
#                 collect_pascal_outputs(pascal_input_geneSet_file, selected_gwas_files)
                return '\n Thanks for using our scoring platform!\n Pathway scoring results will be sent to following email address:\n "{}" '.format(input_value)
            else:
                    return 'Enter a valid gene list!'
        else:
            return 'Enter a valid email address!'
         
#     
