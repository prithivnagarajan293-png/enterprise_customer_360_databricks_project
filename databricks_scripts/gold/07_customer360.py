# Databricks notebook source
from pyspark.sql.functions import *

customers = spark.table("retailmart.gold.dim_customer")
fact_sales = spark.table("retailmart.gold.fact_sales")

# COMMAND ----------

customer_sales = fact_sales.groupBy("customer_key").agg(
    countDistinct("order_id").alias("total_orders"),
    sum("line_amount").alias("total_sales"),
    avg("line_amount").alias("average_order_value"),
    sum("quantity").alias("total_items")
)

# COMMAND ----------

customer360 = customers.join(
    customer_sales,
    "customer_key",
    "left"
)

# COMMAND ----------

customer360 = customer360.fillna({
    "total_orders": 0,
    "total_sales": 0,
    "average_order_value": 0,
    "total_items": 0
})

# COMMAND ----------

customer360.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.customer360")

# COMMAND ----------

display(customer360)

customer360.printSchema()

print(customer360.count())