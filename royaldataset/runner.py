import json
from os.path import isfile
import pandas as pd


def namesnumcheck(xlsxdata, fedata):
    print("      - Executing name concurrence check")
    nameoccurrences = pd.DataFrame(columns=['name', 'number', 'ids'])
    for name in xlsxdata['Personnel Name'].unique():
        ids = []
        for num in fedata.index[fedata.name == str(name)].tolist():
            ids.append(fedata.at[num, 'id'])
            nameoccurrences = nameoccurrences.append({
                'name': name,
                'number': fedata['name'].str.count(name).sum(),
                'ids': ids
                }, ignore_index=True)
    return nameoccurrences


def totalscheck(xlsxdata, fedata):
    print("      - Executing total amount check")
    i = 0
    consolidateregistry = pd.DataFrame(columns=['FE-id', 'name', 'FE-amount', 'XLSX-amounts', 'XLSX-total', 'match'])
    for registry in fedata['id'].unique():
        XLSXamounts = []
        for currname in xlsxdata.index[xlsxdata['Personnel Name'] == fedata.at[i, 'name']].tolist():
            XLSXamounts.append(xlsxdata.at[currname, 'Comision Total a Pagar'])
        consolidateregistry = consolidateregistry.append({
            'FE-id': registry,
            'name': fedata.at[i, 'name'],
            'FE-amount': fedata.at[i, 'amountTotal'],
            'XLSX-amounts': XLSXamounts,
            'XLSX-total': str(sum(XLSXamounts)),
            'match': fedata.at[i, 'amountTotal'] == sum(XLSXamounts)
        }, ignore_index=True)
        i = i + 1
    return consolidateregistry


def run(direct):
    print("--------------------Starting data comparison-------------------")
    f = open(direct + 'datapoints.json', )
    data = json.load(f)
    f.close()
    print("\033[92mPersonnel totals check")
    for i in data['datapoints']:
        xfile = direct + i['site'] + "/" + i['intdate'] + " to " + i['fdate'] + '/data-extracted.json'
        ffile = direct + i['site'] + "/" + i['intdate'] + " to " + i['fdate'] + '/fe-summary.json'
        print("\033[92m   - Executing check for: " + i['site'] + " --- Dates: " + i['intdate'] + " to " + i['fdate'])
        if isfile(xfile) and isfile(ffile):
            xlsxdata = pd.read_json(xfile)
            fedata = pd.read_json(ffile)
            if xlsxdata.empty or fedata.empty:
                print("\033[91m     Error while processing comparison for: " + i['site'] + " --- Dates: " + i['intdate'] + " to " + i['fdate'], end='')
                if xlsxdata.empty and fedata.empty:
                    print(" empty files.")
                elif xlsxdata.empty and not fedata.empty:
                    print(" excel file empty, font-end with data.")
                elif fedata.empty and not xlsxdata.empty:
                    print(" front-end file empty, excel with data.")
                else:
                    print(" unknown error.")
            else:
                namesnumcheck(xlsxdata, fedata)
                totalscheck(xlsxdata, fedata)
        else:
            print("\033[91m      - Error while processing comparison, file(s) not found")

