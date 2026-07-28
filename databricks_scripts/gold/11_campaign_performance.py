# Databricks notebook source
campaigns = spark.table("retailmart.gold.dim_campaign")

campaigns.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("retailmart.gold.campaign_performance")