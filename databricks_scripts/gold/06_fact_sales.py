# Databricks notebook source
from pyspark.sql.functions import col

orders = spark.table("retailmart.silver.orders")
order_items = spark.table("retailmart.silver.order_items")

dim_customer = spark.table("retailmart.gold.dim_customer")
dim_product = spark.table("retailmart.gold.dim_product")
dim_store = spark.table("retailmart.gold.dim_store")
dim_employee = spark.table("retailmart.gold.dim_employee")

# COMMAND ----------

fact_df = orders.join(
    order_items,
    "order_id",
    "inner"
)

# COMMAND ----------

fact_df = fact_df.join(
    dim_customer.select("customer_key", "customer_id"),
    "customer_id",
    "left"
)

# COMMAND ----------

fact_df = fact_df.join(
    dim_product.select("product_key", "product_id"),
    "product_id",
    "left"
)

# COMMAND ----------

fact_df = fact_df.join(
    dim_store.select("store_key", "store_id"),
    "store_id",
    "left"
)

# COMMAND ----------

fact_df = fact_df.join(
    dim_employee.select("employee_key", "employee_id"),
    "employee_id",
    "left"
)

# COMMAND ----------

fact_df = fact_df.select(
    "order_item_id",
    "order_id",

    "customer_key",
    "product_key",
    "store_key",
    "employee_key",

    "order_timestamp",
    "payment_method",
    "order_status",

    "quantity",
    "unit_price",
    "discount",
    "line_amount",

    "is_weekend",
    "order_year",
    "order_month",
    "order_hour"
)

# COMMAND ----------

fact_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("retailmart.gold.fact_sales")

# COMMAND ----------

gold_df = spark.table("retailmart.gold.fact_sales")

display(gold_df)

gold_df.printSchema()

print("Row Count:", gold_df.count())