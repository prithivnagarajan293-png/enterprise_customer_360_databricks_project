# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.silver.products")

display(df)

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

window = Window.orderBy("product_id")

df = df.withColumn(
    "product_key",
    row_number().over(window)
)

# COMMAND ----------

cols = ["product_key"] + [
    c for c in df.columns
    if c != "product_key"
]

df = df.select(cols)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.dim_product")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.dim_product")

display(gold_df)

gold_df.printSchema()

print("Row Count:", gold_df.count())