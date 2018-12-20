import os
import csv
import time
import sys


path_to_pascal_output = '/var/www/FlaskApp/FlaskApp/pascal_output/'
pascal_setting_file_name = 'settings_leaderboard_v3.txt'
path_to_gwas = '/var/www/FlaskApp/data/pascal_scoring/gwasCollection_snpPvals_v1'
path_to_geneScores='/var/www/FlaskApp/data/pascal_scoring/geneScores'
pascal_command = '\
                /var/www/FlaskApp/pascal/Pascal\
                --pval='+path_to_gwas+'gwas_file_name\
                --genescorefile='+path_to_geneScores+'gene_score_file_name\
                --genesetfile=geneset_file_name\
                --outdir='+path_to_pascal_output+\
                '\t--set='+pascal_setting_file_name+\
                '\t--runpathway=on\
                --genescoring=sum\
                '
pascal_input_args = ['gwas_file_name','gene_score_file_name','geneset_file_name']
def generate_pascal_command(pascal_input_dict):
    new_pascal_command = pascal_command
    for i,j in list(pascal_input_dict.items()):
        new_pascal_command = new_pascal_command.replace(i, j)
    return new_pascal_command   

def is_pascal_done(gene_set_file_name,selected_gwas):
    number_of_GWAS = len(selected_gwas)
    print("is_pascal_done:",gene_set_file_name)
    gene_set_file = os.path.splitext(os.path.basename(gene_set_file_name))[0]
    print(os.path.splitext(gene_set_file_name)[0])
    print("\nChecking the processes for geneSet: %s"%(gene_set_file))
    pascal_files=[]
    for g in selected_gwas:
        pascal_files += [ f for f in os.listdir(path_to_pascal_output) if g+ ".PathwaySet--" +gene_set_file in f ]
    if len(pascal_files)==number_of_GWAS:
        print("\nPascal jobs are done!")
        return True
    else:
        print('\nPascal scoring incomplete!')
        return False
    ##
def collect_pascal_outputs(gene_set_file_name,selected_gwas): 
    res =[]
    gene_set_file = os.path.splitext(os.path.basename(gene_set_file_name))[0]
    output_file_name = path_to_pascal_output+'/all_gwas_pathwayScores.'+gene_set_file+'.txt'
    with open(output_file_name,'wb') as csvfile:
        csv_writer= csv.writer(csvfile,delimiter='\t')
        csv_writer.writerow(['gwas_name','pvalue'])
        for g in selected_gwas:
            filename =  g+".PathwaySet--" +gene_set_file+'--sum.txt'
            path2 =os.path.join(path_to_pascal_output,filename)  
            L = csv.reader( open(path2, 'rU'),delimiter='\t')
            next(L)
            for a in L:
                if a[1]!='NA':
                    res.append([g,float(a[1])])
                    csv_writer.writerow([g,float(a[1])])
    return res

def run_pascal(gene_set_file_name,selected_gwas_list):
    print("Sarting pascal jobs: ")
    path_to_error_output = os.path.join(path_to_pascal_output,'job_submission_output')  
    basename = os.path.splitext(os.path.basename(gene_set_file_name))[0] #1_ppi_anonym_v2
    ### background annotation file: settings_leaderboard_v3 (all coding gene)
    for gwas in selected_gwas_list:
        gwas_file_name=gwas+'.txt.gz'
        genescore_file_name = gwas+'.sum.genescores.txt'
        scriptcommand = generate_pascal_command(dict(list(zip(pascal_input_args,[gwas_file_name,genescore_file_name,gene_set_file_name]))))
        print("\n Submitting job for running pacal,",os.getpid(),":",scriptcommand)
        os.system(scriptcommand)

if __name__ == '__main__':
    submission_file = sys.argv[1]
    selected_gwas_list = sys.argv[2]
    run_pascal(submission_file, selected_gwas_list)
    while not is_pascal_done(submission_file, selected_gwas_list):
        time.sleep(10)
    print("Collecting results")
    collect_pascal_outputs(submission_file, selected_gwas_list)