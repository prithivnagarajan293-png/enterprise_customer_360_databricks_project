# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.bronze.employees")

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

df.groupBy("employee_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

display(df.select("role").distinct())

# COMMAND ----------

display(df.select("store_id").distinct())

# COMMAND ----------

from pyspark.sql.functions import trim, col
from pyspark.sql.types import StringType

for field in df.schema.fields:
    if isinstance(field.dataType, StringType):
        df = df.withColumn(field.name, trim(col(field.name)))

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

df = df.withColumn(
    "processed_timestamp",
    current_timestamp()
)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.silver.employees")

# COMMAND ----------

silver_df = spark.table("retailmart.silver.employees")

display(silver_df)

silver_df.printSchema()