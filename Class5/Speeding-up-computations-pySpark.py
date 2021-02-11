# Databricks notebook source
# Per https://stackoverflow.com/questions/57014043/reading-data-from-url-using-spark-databricks-platform
from pyspark import SparkFiles

# COMMAND ----------

URL = "https://s3.amazonaws.com/h2o-airlines-unpacked/year2012.csv"

# COMMAND ----------

# Per https://stackoverflow.com/questions/57014043/reading-data-from-url-using-spark-databricks-platform
spark.sparkContext.addFile(url)
df_spark = spark.read.csv("file://"+SparkFiles.get("year2012.csv"), header=True, inferSchema= True)

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
