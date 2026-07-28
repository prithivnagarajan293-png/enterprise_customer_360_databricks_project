# Databricks notebook source
from pyspark.sql.functions import *

products = spark.table("retailmart.gold.dim_product")
fact_sales = spark.table("retailmart.gold.fact_sales")

# COMMAND ----------

product_sales = fact_sales.groupBy("product_key").agg(
    sum("quantity").alias("units_sold"),
    sum("line_amount").alias("total_sales"),
    avg("line_amount").alias("average_sale"),
    countDistinct("order_id").alias("total_orders")
)

# COMMAND ----------

product_performance = products.join(
    product_sales,
    "product_key",
    "left"
)

# COMMAND ----------

product_performance.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("retailmart.gold.product_performance")