# Geo_OD_data
#### 清洗信令OD

geodata.py 从数亿条OD数据中取出O==D的条目

1.使用osgeo.ogr从Geodatabase取出layer
2.对layer中feature做循环迭代
3.连接SQL数据库，并逐条上传

