import pymysql
import geopandas as gpd
import pandas as pd
import os
from osgeo import ogr
import sys
from time import time
from pymysql.connections import DEFAULT_CHARSET


'''
help(ogr)
https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
'''

#Get featureList in GDB
# featsClassList = []
# for featsClass_idx in range(gdb.GetLayerCount()):
#     featsClass = gdb.GetLayerByIndex(featsClass_idx)
#     featsClassList.append(featsClass.GetName())
# featsClassList.sort()
# for featsClass in featsClassList:
#     print (featsClass)

#Iterate in features
# m = 0
# for feature in data:
#     m += 1
#     print (feature.GetField("START_H"))
#     if m == 10:
#         break

# sql = 'select * from student'

'''
Get Layer
'''
file = r'D:\data\***\5od_hour.gdb'
driver = ogr.GetDriverByName("OpenFileGDB")
gdb = driver.Open(file, 0)
data = gdb.GetLayer('od_508_521')

'''
Count features
'''
featureCount = data.GetFeatureCount()
print ("...1.Number of features in %s: %d" 
        % (os.path.basename(file),featureCount))

'''
Get column names
'''
layerDefinition = data.GetLayerDefn()
colum = ''
fields = []
for i in range(layerDefinition.GetFieldCount()):
    name = layerDefinition.GetFieldDefn(i).GetName()
    fields.append(name)
    colum = colum + name + ' varchar(255),'
print('...2.Fields is: %s' % fields)
print('.....Laryer is: %s' % type(data))


'''
connected to SQL
'''
config = {'host' : '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': '***',
            'database': "test",
        #   'charset': 'utf8mb4',
            'local_infile': 1
            }
conn = pymysql.connect(**config)
cur = conn.cursor()
print('...3.Connected sql to %s' % type(conn))


'''
[first time run] define OD_table
'''
# cur.execute('DROP TABLE IF EXISTS OD_table')
# sql = """CREATE TABLE OD_table (
#         O_BMID  CHAR(20),
#         D_BMID  CHAR(20),
#         START_H CHAR(20),
#         CNT INT,
#         USER_CNT INT)"""
# cur.execute(sql)

'''
iterate in features
upload to Sql
'''
m = 0
for feature in data:
    m += 1
    if m % 1000000 ==0: 
        print('.....%d/300' % (m/1000000))
    if feature.GetField("O_BMID") == feature.GetField("D_BMID"):
        sql = 'INSERT INTO OD_table(O_BMID,\
            D_BMID, START_H, CNT, USER_CNT)\
            VALUES (%s, %s, %s, %s, %s)'
        cur.execute(sql, (
                          feature.GetField("O_BMID"),
                          feature.GetField("D_BMID"),
                          feature.GetField("START_H"),
                          feature.GetField("CNT"),
                          feature.GetField("USER_CNT")
                          )
                    )
cur.close()
conn.commit()
print('good')


