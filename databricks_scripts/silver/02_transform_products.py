# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.bronze.products")

display(df)

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col, count, when

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).display()

# COMMAND ----------

df.groupBy("product_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df.select("category").distinct())

# COMMAND ----------

display(df.select("brand").distinct())

# COMMAND ----------

from pyspark.sql.functions import trim, col
from pyspark.sql.types import StringType

for field in df.schema.fields:
    if isinstance(field.dataType, StringType):
        df = df.withColumn(field.name, trim(col(field.name)))

print("Whitespace trimmed.")

# COMMAND ----------

from pyspark.sql.functions import when, col

df = df.withColumn(
    "brand",
    when(col("brand").isNull(), "Unknown")
    .otherwise(col("brand"))
)

print("Missing brands replaced.")

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
    .saveAsTable("retailmart.silver.products")

# COMMAND ----------

silver_df = spark.table("retailmart.silver.products")

display(silver_df)

silver_df.printSchema()