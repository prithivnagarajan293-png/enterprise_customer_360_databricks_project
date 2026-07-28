# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.silver.customers")

display(df)

df.printSchema()

# COMMAND ----------

print(df.count())
display(df.limit(10))

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

df = spark.table("retailmart.silver.customers")

display(df)

# COMMAND ----------

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

window = Window.orderBy("customer_id")

df = df.withColumn(
    "customer_key",
    row_number().over(window)
)

# COMMAND ----------

cols = ["customer_key"] + [
    c for c in df.columns
    if c != "customer_key"
]

df = df.select(cols)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.dim_customer")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.dim_customer")

display(gold_df)

gold_df.printSchema()

# COMMAND ----------

print("Row Count:", gold_df.count())