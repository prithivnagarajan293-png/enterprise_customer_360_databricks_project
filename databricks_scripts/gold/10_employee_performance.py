# Databricks notebook source
from pyspark.sql.functions import *

employees = spark.table("retailmart.gold.dim_employee")
fact_sales = spark.table("retailmart.gold.fact_sales")

employee_sales = fact_sales.groupBy("employee_key").agg(
    countDistinct("order_id").alias("orders_handled"),
    sum("line_amount").alias("total_sales"),
    avg("line_amount").alias("average_sale")
)

employee_performance = employees.join(
    employee_sales,
    "employee_key",
    "left"
).fillna({
    "orders_handled":0,
    "total_sales":0,
    "average_sale":0
})

employee_performance.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("retailmart.gold.employee_performance")