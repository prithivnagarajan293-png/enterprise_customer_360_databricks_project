# Databricks notebook source
from pyspark.sql import functions as F

# Read Bronze customer table
df = spark.table("retailmart.bronze.customers")

# Display sample data
display(df)

# Display schema
df.printSchema()

# COMMAND ----------

display(
    df.select("annual_income") 
)

# COMMAND ----------

from pyspark.sql.functions import col, count, when

df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
]).display()

# COMMAND ----------

df.groupBy("customer_id") \
  .count() \
  .filter("count > 1") \
  .display()

# COMMAND ----------

display(df.select("customer_segment").distinct())

# COMMAND ----------

display(df.select("loyalty_level").distinct())

# COMMAND ----------

display(df.select("preferred_channel").distinct())

# COMMAND ----------

from pyspark.sql.functions import trim, col
from pyspark.sql.types import StringType

# Trim all string columns
for field in df.schema.fields:
    if isinstance(field.dataType, StringType):
        df = df.withColumn(field.name, trim(col(field.name)))

print("Whitespace trimmed from all string columns.")

# COMMAND ----------

from pyspark.sql.functions import col

df = df.withColumn(
    "phone",
    col("phone").cast("string")
)

print("Phone column converted to string.")


# COMMAND ----------

df.printSchema()

# COMMAND ----------

before_count = df.count()

df = df.dropDuplicates(["customer_id"])

after_count = df.count()

print(f"Rows before deduplication : {before_count}")
print(f"Rows after deduplication  : {after_count}")
print(f"Duplicates removed        : {before_count - after_count}")

# COMMAND ----------

from pyspark.sql.functions import col, when

df = df.withColumn(
    "city",
    when(col("city").isNull(), "Unknown")
    .otherwise(col("city"))
)

print("Missing city values replaced with 'Unknown'.")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

df = df.withColumn(
    "processed_timestamp",
    current_timestamp()
)

print("Audit column added.")

# COMMAND ----------

display(
    df.select(
        "customer_id",
        "processed_timestamp"
    )
)

# COMMAND ----------

# Write cleaned data to Silver layer

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.silver.customers")

print("Silver customer table created successfully.")

# COMMAND ----------

silver_df = spark.table("retailmart.silver.customers")

display(silver_df)

silver_df.printSchema()

# COMMAND ----------

print("Silver rows:", silver_df.count())

# COMMAND ----------

display(
    silver_df.groupBy("customer_id")
             .count()
             .filter("count > 1")
)

# COMMAND ----------

display(
    silver_df.filter(F.col("city") == "Unknown")
)

# COMMAND ----------

silver_df.printSchema()