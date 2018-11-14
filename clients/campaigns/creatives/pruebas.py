#import json
#from util.config import modelConfig
#from util.functions.funtions import db_functions

# clients = '''
#        [{ "email" : "HUASTECAS@gmail.com","name" : "MOISES JOSUE ALCANTARA CABADILLA","password" : "ALCANTARA", "cpm" : "1",
#        "budget" : "15000.90", "company" : "AUTOTRANSPORTES RAPIDOS DOS HUASTECAS S A DE C V", "rfc" : "ASS001002KX0",
#        "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
#        "phone" : "3125256987"
#        },
#        { "email" : "ECOLOGICOS@gmail.com","name" : "PEDRO ALBERTO ARAMBURA CONTRERAS" ,"password" : "ARAMBURA", "cpm" : "18",
#        "budget" : "10000.52", "company" : "ASESORIA Y SERVICIOS ECOLOGICOS INTEGRALES S.A.", "rfc" : "ASE0009266M0",
#        "address" : "BRONCE #9326 CD INDUSTRIAL MITRAS GARCIA N.L. C.P. 66000",
#        "phone" : "3128256987"
#        }]'''
#
# info = json.loads(clients)
#
# code = """
# info = {0}
# print(info)
# cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[1]['rfc'])
# sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, password, company_name, rfc, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'
# val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'],info[0]['address'])
# cur.execute(sql, val)
# """.format(info)
#
# db_functions(code)

"""
import csv
csv_list = []
with open('C:/Pruebas android/cerebro/util/creatives/creatives1OK .csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    title = reader.__next__()
    for row in reader:
        listcsv = {}
        for column in range(len(title)):
            listcsv[title[column]] = row[column]
        csv_list.append(listcsv)
    print(csv_list[0])
"""
from util.functions import db_functions

list_creatives = [
    {"name": "Compra ahorra", "status": 1, "measure": "10x10", "url": "http://www.algo.com", "type": "IMAGE"},
    {"name": "Compra gasta", "status": 0, "measure": "5x15", "url": "http://www.compraalgo.com", "type": "HTML5"},
    {"name": "Promo 1", "status": 1, "measure": "3x18", "url": "http://www.promoalgo.com", "type": "GIF"}
]

code = """
campaign = {1}
list_creatives = {0}
for creative in list_creatives:
    cur.execute("DELETE FROM creatives WHERE campaign_id = %d AND name = '%s';" % (campaign,creative["name"]))
rand = random.randint(0, len(list_creatives)-1)
cur.execute("INSERT INTO creatives (name,url,measure,type,status,created_at,updated_at,campaign_id) VALUES "
            "('%s','%s','%s','%s',%d,current_timestamp,current_timestamp,%d) RETURNING id;" 
            % (list_creatives[rand]["name"],list_creatives[rand]["url"],list_creatives[rand]["measure"],
               list_creatives[rand]["type"],list_creatives[rand]["status"],campaign))
id = cur.fetchone()[0]
cur.execute("UPDATE creatives SET creative_code = '%s-%d', "
            "redirect_url = 'https://hnz3ccup03.execute-api.us-west-2.amazonaws.com/stage/"
            "redirect?ca=PRUEBA-2&ct=CESAR-17&adUrl=http://www.arca-stage.vjdbsvf9qh.us-west-2.elasticbeanstalk.com"
            "/customer/dashboard', script_snippet = '<script id=cer-tracking src=https://d260gejhgij5g1.cloudfront.net/"
            "js/libs/cer.min.js?ca=PRUEBA-2&ct=CESAR-17></script>' "
            "WHERE ID = %d RETURNING id;"
            % (list_creatives[rand]["name"].upper(), id, id))
""".format(list_creatives,10)
creative = db_functions(code)[0][0]
print(creative)