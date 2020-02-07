# Databricks notebook source
import urllib.request

# COMMAND ----------

file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year2012.csv"

# COMMAND ----------

### --- Read-in dataset by first moving file to cluster's local storage
# Download file, per https://docs.databricks.com/_static/notebooks/zip-files-python.html:
urllib.request.urlretrieve(file_name, '/tmp/df.csv')

# Move file per to DBFS, per https://docs.databricks.com/_static/notebooks/zip-files-python.html:
dbutils.fs.mv("file:/tmp/df.csv", "dbfs:/data/df.csv")

# Per https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#datasets-and-dataframes, 'spark' is an existing SparkSession:
df_spark = spark.read.format('csv').options(header='true', inferSchema='true').load('dbfs:/data/df.csv')

# COMMAND ----------

display(df_spark)

# COMMAND ----------

# --- Make dataframe available to run SQL queries against:
df_spark.createOrReplaceTempView("df_spark")

# COMMAND ----------

df_carrier_counts = spark.sql("""SELECT uniquecarrier, count(*) as N
                                 FROM df_spark
                                 GROUP BY uniquecarrier
                                 ORDER BY uniquecarrier""")
df_carrier_counts.show()
