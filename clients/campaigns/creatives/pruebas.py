# import json
# from util.config import ModelConfig
# from util.functions.funtions import db_functions

#  clients = '''
#         [{ "email" : "HUASTECAS@gmail.com","name" : "MOISES JOSUE ALCANTARA CABADILLA","password" : "ALCANTARA", "cpm" : "1",
#         "budget" : "15000.90", "company" : "AUTOTRANSPORTES RAPIDOS DOS HUASTECAS S A DE C V", "rfc" : "ASS001002KX0",
#         "address" : "2 DE ABRIL NUM 1022 ORIENTE COL INDEPENDENCIA MONTERREY N L",
#         "phone" : "3125256987"
#         },
#         { "email" : "ECOLOGICOS@gmail.com","name" : "PEDRO ALBERTO ARAMBURA CONTRERAS" ,"password" : "ARAMBURA", "cpm" : "18",
#         "budget" : "10000.52", "company" : "ASESORIA Y SERVICIOS ECOLOGICOS INTEGRALES S.A.", "rfc" : "ASE0009266M0",
#         "address" : "BRONCE # 9326 CD INDUSTRIAL MITRAS GARCIA N.L. C.P. 66000",
#         "phone" : "3128256987"
#         }]'''
# 
#  info = json.loads(clients)
# 
#  code = """
#  info = {0}
#  print(info)
#  cur.execute("DELETE FROM clients WHERE rfc = '%s'" % info[1]['rfc'])
#  sql = 'INSERT INTO clients (person_contact, cpm, budget, status, email, "createdAt", updated_at, password, company_name, rfc, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'
#  val = (info[0]['name'], info[0]['cpm'], info[0]['budget'], 1, info[0]['email'], strftime("%Y/%m/%d"), strftime("%Y/%m/%d"), info[0]['password'], info[0]['company'], info[0]['rfc'], info[0]['phone'],info[0]['address'])
#  cur.execute(sql, val)
#  """.format(info)
# 
#  db_functions(code)

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
import os

home = file_path = ((os.getenv('USERPROFILE') or os.getenv('HOME'))+"\Downloads\creatives.csv").replace("\\", "\\\\")
print(home)