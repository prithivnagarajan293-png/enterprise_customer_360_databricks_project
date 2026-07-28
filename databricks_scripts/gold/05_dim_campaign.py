# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.silver.marketing_campaigns")

display(df)

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

window = Window.orderBy("campaign_id")

df = df.withColumn(
    "campaign_key",
    row_number().over(window)
)

# COMMAND ----------

cols = ["campaign_key"] + [
    c for c in df.columns
    if c != "campaign_key"
]

df = df.select(cols)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.dim_campaign")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.dim_campaign")

display(gold_df)

gold_df.printSchema()

print("Row Count:", gold_df.count())