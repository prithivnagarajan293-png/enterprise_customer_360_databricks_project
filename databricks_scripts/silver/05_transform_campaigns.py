# Databricks notebook source
spark.sql("SHOW TABLES IN retailmart.bronze").display()

# COMMAND ----------

display(spark.sql("SHOW CATALOGS"))

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.table("retailmart.bronze.marketing_campaigns")

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

df.groupBy("campaign_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

display(df.select("campaign_type").distinct())

# COMMAND ----------

display(df.select("budget").distinct())

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
    .saveAsTable("retailmart.silver.marketing_campaigns")

# COMMAND ----------

silver_df = spark.table("retailmart.silver.marketing_campaigns")

display(silver_df)

silver_df.printSchema()