# Databricks notebook source
from pyspark.sql.functions import *

stores = spark.table("retailmart.gold.dim_store")
fact_sales = spark.table("retailmart.gold.fact_sales")

store_sales = fact_sales.groupBy("store_key").agg(
    countDistinct("order_id").alias("total_orders"),
    sum("line_amount").alias("total_sales"),
    avg("line_amount").alias("average_sale"),
    sum("quantity").alias("items_sold")
)

store_performance = stores.join(
    store_sales,
    "store_key",
    "left"
).fillna({
    "total_orders":0,
    "total_sales":0,
    "average_sale":0,
    "items_sold":0
})

store_performance.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("retailmart.gold.store_performance")