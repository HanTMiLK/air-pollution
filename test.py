# -*- coding: utf-8 -*-
import json
import requests
import pyspark
import os,io
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext,SparkSession
from pyspark.sql.types import Row,StructField,StructType,StringType,IntegerType


if __name__=="__main__":
	r = requests.get("https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json")
	data = r.json()
	datajs = data['records']
	with open('example.json','w') as f:
		j=json.dumps(datajs)
		j.strip(' ')
		f.write(j)
	os.system("hadoop fs -copyFromLocal -f /home/dmcl/python_web/example.json /user/wolf/example.json")
	sc = SparkContext()
	sqlContext = SQLContext(sc)
	so=sc.parallelize(data)
	df=sqlContext.read.json("hdfs://410685023master:9000/user/wolf/example.json")
	print(df.printSchema())
	df=df.withColumnRenamed("PM2.5","PM25")
	aqi1=df.groupby('County').agg({u"AQI":'mean'}).sort("avg(AQI)",ascending=False).rdd.map(lambda x: x[0])
	aqi2=df.groupby('County').agg({u"AQI":'mean'}).sort("avg(AQI)",ascending=False).rdd.map(lambda x: x[1])
	PM251=df.groupby('County').agg({u"PM25":"mean"}).sort(u"avg(PM25)",ascending=False).rdd.map(lambda x:x[0])
	PM252=df.groupby('County').agg({u"PM25":"mean"}).sort(u"avg(PM25)",ascending=False).rdd.map(lambda x:x[1])
	aa=aqi1.collect()
	ba=aqi2.collect()
	aqijsdict = dict(zip(aa,ba))
	aqijs=json.dumps(aqijsdict, ensure_ascii=False, sort_keys=False,indent=4)
	pa=PM251.collect()
	pb=PM252.collect()
	PM25dict = dict(zip(pa,pb))
	PM2js=json.dumps(PM25dict, ensure_ascii=False, sort_keys=False,indent=4)

	with io.open('./static/aqi.js','w',encoding='UTF-8') as f:
		t="var aqi="
   	 	f.write(t.decode('UTF-8'))
   	 	f.write(aqijs)
	with io.open('./static/PM2.js','w',encoding='UTF-8') as fw:
		tt="var PM="
   	 	fw.write(tt.decode('UTF-8'))
    		fw.write(PM2js)
