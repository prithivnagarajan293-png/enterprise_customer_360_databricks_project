# Databricks notebook source
# ==========================================
# Bronze Layer Configuration
# Enterprise Customer 360 Lakehouse
# ==========================================

RAW_DATA_PATH = "/Volumes/retailmart/raw_csv/csv_files"

BRONZE_SCHEMA = "retailmart.bronze"

CUSTOMERS = {
    "name": "customers",
    "source": f"{RAW_DATA_PATH}/customers.csv",
    "target": f"{BRONZE_SCHEMA}.customers"
}

PRODUCTS = {
    "name": "products",
    "source": f"{RAW_DATA_PATH}/products.csv",
    "target": f"{BRONZE_SCHEMA}.products"
}

STORES = {
    "name": "stores",
    "source": f"{RAW_DATA_PATH}/stores.csv",
    "target": f"{BRONZE_SCHEMA}.stores"
}

EMPLOYEES = {
    "name": "employees",
    "source": f"{RAW_DATA_PATH}/employees.csv",
    "target": f"{BRONZE_SCHEMA}.employees"
}

CAMPAIGNS = {
    "name": "marketing_campaigns",
    "source": f"{RAW_DATA_PATH}/marketing_campaigns.csv",
    "target": f"{BRONZE_SCHEMA}.marketing_campaigns"
}

ORDERS = {
    "name": "orders",
    "source": f"{RAW_DATA_PATH}/orders.csv",
    "target": f"{BRONZE_SCHEMA}.orders"
}

ORDER_ITEMS = {
    "name": "order_items",
    "source": f"{RAW_DATA_PATH}/order_items.csv",
    "target": f"{BRONZE_SCHEMA}.order_items"
}

print("Bronze configuration loaded successfully.")

# COMMAND ----------

print(CUSTOMERS)