import os
import pandas as pd
import requests
import json


def gettoken():
    url = 'http://agile-qk.com:50003/auth/oauth/token'
    headers = {'Authorization': 'Basic c2Nzdm06Y2xpZW50U2VjcmV0','Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        "grant_type": "password",
        'username': "appComVtaMkt",
        'password': "U2FsdGVkX19ezrtZgbiBnEdw2tIpkKB9fNLasRJoVBc%3D"
        }
    r = requests.post(url, headers=headers, data=payload, verify=False, allow_redirects=False)
    token = json.loads(r.text)
    return token


def getabstract(headers, srid, commaname, systemid, idate, fdate):
    url = 'http://agile-qk.com:50003/catalog/income/filter'
    if srid == 'acapulco':
        sridno = '829'
    elif srid == 'mazatlan':
        sridno = '691'
    payload = {
        'saleRoomId': sridno,
        'commissionAgentName': commaname,
        'systemId': systemid,
        'initialDate': idate,
        'finalDate': fdate
    }
    r = requests.get(url, headers=headers, params=payload)
    abstract = json.loads(r.text)
    return abstract


def getcomdet(headers, srid, file, commia, commaid, incoid, idate, fdate):
    url = 'http://agile-qk.com:50003/catalog/amount-detail/sale/search'
    if srid == 'acapulco':
        sridno = '829'
    elif srid == 'mazatlan':
        sridno = '691'
    payload = {
        'saleRoomId': sridno,
        'file': file,
        'commissionAgent': commia,
        'commissionAgentId': commaid,
        'incomeId': incoid,
        'startDate': idate,
        'finalDate': fdate
    }
    r = requests.get(url, headers=headers, params=payload)
    comdet = json.loads(r.text)
    return comdet


def getcontractdetail(headers, srid, file, idate, fdate):
    url = 'http://agile-qk.com:50003/catalog/amount-detail/sale-file'
    payload = {
        'saleRoomId': srid,
        'fileId': file,
        'startDate': idate,
        'finalDate': fdate
    }
    r = requests.get(url, headers=headers, params=payload)
    condet = json.loads(r.text)
    return condet


def run(dire):
    print("--------------------Starting front-end query-------------------")
    token = gettoken()
    headers = {
        'authorization': 'Bearer '+token['access_token'],
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    f = open(dire + 'datapoints.json', 'r')
    dp = json.load(f)
    print("Comission sumary query:")

    for x in dp['datapoints']:
        summary = {}
        idate = x['intdate'].split("-")
        fdate = x['fdate'].split("-")
        startdate = idate[2]+"-"+idate[1]+"-"+idate[0]
        finaldate = fdate[2] + "-" + fdate[1] + "-" + fdate[0]
        personneldir = dire + x['site'] + "/" + x['intdate'] + " to " + x['fdate'] + "/personnel/"
        os.mkdir(personneldir)
        os.mkdir(personneldir + "/comm-detail/")
        print("   - Executing query for site: " + x['site'] + " --- Dates: " + x['intdate'] + " to " + x['fdate'])
        summary['data'] = getabstract(headers, x['site'], "", "1", startdate, finaldate)
        with open(dire + x['site'] + "/" + x['intdate'] + " to " + x['fdate'] + '/fe-summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
        print("      - Results saved as: " + x['site'] + "/" + x['intdate'] + " to " + x['fdate'] + '/fe-summary.json')
        for i in summary['data']:
            print("      - Executing query for detail of commision: " + str(i['id']))
            os.mkdir(personneldir + "/comm-detail/"+str(i['commissionAgentId']))
            commdetail = getcomdet(headers, x['site'], "", i['name'], i['commissionAgentId'], i['id'], startdate, finaldate)
            with open(personneldir + "/comm-detail/"+str(i['commissionAgentId']) + '/comm-detail.json', 'w', encoding='utf-8') as f:
                json.dump(commdetail, f, ensure_ascii=False, indent=4)
            print("         - Commission detail for: " + str(i['id']) + " Saved in: " + personneldir + "comm-detail/"+str(i['commissionAgentId']) + '/comm-detail.json')
        print("   - writing master trace file: " + str(i['id']))
        commissioners = []
        for i in summary['data']:
            commissioners.append(i['commissionAgentId'])
        commiids = pd.unique(commissioners).tolist()
        commissioners = pd.DataFrame(columns=['id', 'name', 'commissions'])
        #main =
        for cid in commiids:

            commissioners = commissioners.append({
                'id': cid,
                'name': 'test',
                'commissions': 'test'
            }, ignore_index=True)
        print(commissioners)
    print("--------------------Front-end query complete-------------------\n")
