import pandas as pd
import json
import numpy as np


def acapulco(xlsx_file):
    dfs = pd.read_excel(xlsx_file, sheet_name='Ventas para Nomina v1.1', header=1)
    for col in dfs.columns:
        if 'Unnamed' in col:
            dfs = dfs.drop(columns=[col])
    dfs = dfs.fillna(value=np.nan)
    dfs.dropna(subset=['Personnel Name', 'Site Name', 'Comision Total a Pagar'], inplace=True, how='all')
    for index, row in dfs.iterrows():
        if pd.isna(row['Personnel Name']) and pd.isna(row['Site Name']) and pd.isna(row['Site Name']):
            dfs.drop([index], inplace=True)
    dfs.reset_index(drop=True, inplace=True)
    return dfs


def run(direct):
    print("--------------------Starting data extraction-------------------")
    f = open(direct + 'datapoints.json', )
    data = json.load(f)
    f.close()
    for i in data['datapoints']:
        print("Processing " + i['datafile'] + " --- Site: " + i['site'])
        filename = direct + i['site'] + "/" + i['intdate'] + " to " + i['fdate'] + '/data-extracted.json'
        if i['site'] == 'acapulco':
            exdata = acapulco("Data/" + i['site'] + "/" + i['datafile'])
            exdata.to_json(path_or_buf=filename, orient='records', force_ascii=False, indent=4)
            print('   - Data saved as: ' + filename)
    print("--------------------Data extraction complete-------------------\n")
