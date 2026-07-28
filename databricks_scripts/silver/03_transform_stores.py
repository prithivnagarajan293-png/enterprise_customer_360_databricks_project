# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.bronze.stores")

display(df)

df.printSchema()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col, count, when

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).display()

# COMMAND ----------

df.groupBy("store_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

display(df.select("store_id").distinct())

# COMMAND ----------

display(df.select("state").distinct())

# COMMAND ----------

display(df.select("region").distinct())

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.silver.stores")

# COMMAND ----------

spark.table("retailmart.silver.orders").printSchema()