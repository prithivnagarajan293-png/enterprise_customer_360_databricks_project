# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.silver.employees")

display(df)

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

window = Window.orderBy("employee_id")

df = df.withColumn(
    "employee_key",
    row_number().over(window)
)

# COMMAND ----------

cols = ["employee_key"] + [
    c for c in df.columns
    if c != "employee_key"
]

df = df.select(cols)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.dim_employee")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.dim_employee")

display(gold_df)

gold_df.printSchema()

print("Row Count:", gold_df.count())