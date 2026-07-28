# Databricks notebook source
spark.sql("SHOW TABLES IN retailmart.silver").display()

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.table("retailmart.silver.stores")

display(df)

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

window = Window.orderBy("store_id")

df = df.withColumn(
    "store_key",
    row_number().over(window)
)

# COMMAND ----------

cols = ["store_key"] + [
    c for c in df.columns
    if c != "store_key"
]

df = df.select(cols)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.dim_store")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.dim_store")

display(gold_df)

gold_df.printSchema()

print("Row Count:", gold_df.count())