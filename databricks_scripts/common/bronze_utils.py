# Databricks notebook source
# ==========================================
# Bronze Utility Functions
# Enterprise Customer 360 Lakehouse
# ==========================================

def ingest_to_bronze(config):

    dataset_name = config["name"]
    source_path = config["source"]
    target_table = config["target"]

    print("=" * 60)
    print(f"Starting Bronze ingestion : {dataset_name}")
    print("=" * 60)

    print(f"Source : {source_path}")
    print(f"Target : {target_table}")

    # Read CSV
    df = (
        spark.read
            .format("csv")
            .option("header", "true")
            .option("inferSchema", "true")
            .load(source_path)
    )

    source_rows = df.count()

    print(f"Rows Read : {source_rows}")

    if source_rows == 0:
        raise Exception("Source file is empty.")

    print("\nSchema:")
    df.printSchema()

    (
        df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(target_table)
    )

    bronze_df = spark.table(target_table)

    bronze_rows = bronze_df.count()

    if bronze_rows != source_rows:
        raise Exception(
            f"Row count mismatch. Source={source_rows}, Target={bronze_rows}"
        )

    print("Data quality validation passed.")

    display(bronze_df.limit(10))

    print("=" * 60)
    print("Bronze Ingestion Completed Successfully")
    print("=" * 60)
    print(f"Dataset : {dataset_name}")
    print(f"Rows    : {bronze_rows}")