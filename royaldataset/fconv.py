import json
import os


def run(dire):
    print("------------------Starting data points parsing-----------------")
    print("Data points found:")
    data = {'datapoints': []}
    meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    m = ""
    mi = ""
    dates = []
    f = open(dire+'files.json', 'r')
    files = json.load(f)
    for i in files['files']:
        for mes in meses:
            if mes in i['file'].upper():
                mi = str(meses.index(mes) + 1)
                m = mes
                if len(mi) == 1:
                    mi = "0" + mi
        if i['site'] == 'acapulco':
            dates = i['file']\
                    .replace("NOMINA", "")\
                    .replace("AL", "-")\
                    .replace("DE", "")\
                    .replace(m, "-"+mi+"-")\
                    .replace(" ", "")\
                    .replace(".xlsx", "").split('-')
        elif i['site'] == 'mazatlan':
            dates = i['file'] \
                    .upper()\
                    .replace("NOM ", "")\
                    .replace(m, "-"+mi+"-")\
                    .replace(" ", "-")\
                    .replace("1RA", "") \
                    .replace("2DA", "") \
                    .replace("MAZATLAN", "") \
                    .replace("QUINCENA", "") \
                    .replace(".XLSX", "")\
                    .split('-')
        while "" in dates:
            dates.remove("")
        for x in range(len(dates)):
            if len(dates[x]) == 1:
                dates[x] = '0' + dates[x]
        if len(dates[3]) == 2:
            dates[3] = "20"+dates[3]
        idate = dates[0]+"-"+dates[2]+"-"+dates[3]
        fdate = dates[1]+"-"+dates[2]+"-"+dates[3]
        tdata = {'site': i['site'], 'datafile': i['file'], 'intdate': idate, 'fdate': fdate}
        data['datapoints'].append(tdata)
        print("   - From: "+dates[0] +
              "/"+dates[2] +
              "/"+dates[3] +
              " To: "+dates[1] +
              "/"+dates[2] +
              "/"+dates[3] +
              " For site: "+i['site']
              )
        os.mkdir(dire + i['site'] + "/" + idate + " to " + fdate)
    with open(dire+'datapoints.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print("Data points exported as : " + dire+'datapoints.json')
    print("------------------Data points parsing complete-----------------\n")
