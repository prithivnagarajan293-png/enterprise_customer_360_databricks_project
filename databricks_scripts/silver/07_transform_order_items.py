# Databricks notebook source
from pyspark.sql import functions as F

df = spark.table("retailmart.bronze.order_items")

display(df)

df.printSchema()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df.select("campaign_type").distinct())

# COMMAND ----------

from pyspark.sql.functions import col, count, when

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).display()

# COMMAND ----------

df.groupBy("order_item_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

display(df.select("order_item_id").distinct())

# COMMAND ----------

display(df.select("discount").distinct())

# COMMAND ----------

display(
    df.filter(col("quantity") < 0)
)

# COMMAND ----------

display(
    df.filter(col("unit_price") < 0)
)

# COMMAND ----------

display(
    df.filter(col("discount") < 0)
)

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
    .saveAsTable("retailmart.silver.order_items")

# COMMAND ----------

silver_df = spark.table("retailmart.silver.order_items")

display(silver_df)

silver_df.printSchema()