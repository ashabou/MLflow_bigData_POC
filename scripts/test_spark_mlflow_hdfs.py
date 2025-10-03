#!/usr/bin/env python3
"""MLflow with PostgreSQL + Spark Local Mode"""

import os
import sys

spark_home = "/opt/spark-3.4.1-bin-hadoop3"
sys.path.insert(0, os.path.join(spark_home, "python"))

from pyspark.sql import SparkSession
import mlflow
import mlflow.spark
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler

print("=" * 60)
print("MLflow + Spark Local Mode + PostgreSQL")
print("=" * 60)

# Spark LOCAL mode (no YARN/HDFS needed)
spark = SparkSession.builder \
    .appName("MLflow-POC") \
    .master("local[*]") \
    .getOrCreate()

print(f"✓ Spark {spark.version} running in local mode")

# PostgreSQL backend
mlflow.set_tracking_uri("postgresql://mlflow_user:strongpassword@localhost/mlflow_db")
mlflow.set_experiment("spark-local-poc")

# Generate data
from pyspark.sql.types import *
schema = StructType([
    StructField("f1", DoubleType()),
    StructField("f2", DoubleType()),
    StructField("f3", DoubleType()),
    StructField("f4", DoubleType()),
    StructField("label", IntegerType())
])

data = [(5.1,3.5,1.4,0.2,0), (4.9,3.0,1.4,0.2,0), (7.0,3.2,4.7,1.4,1),
        (6.4,3.2,4.5,1.5,1), (6.3,3.3,6.0,2.5,2), (5.8,2.7,5.1,1.9,2)] * 20

df = spark.createDataFrame(data, schema)
assembler = VectorAssembler(inputCols=["f1","f2","f3","f4"], outputCol="features")
df = assembler.transform(df)

# Train with MLflow tracking
with mlflow.start_run(run_name="local_test"):
    mlflow.log_param("mode", "local")
    mlflow.log_param("backend", "postgresql")
    
    lr = LogisticRegression(maxIter=10)
    model = lr.fit(df)
    
    predictions = model.transform(df)
    accuracy = predictions.filter(predictions.label == predictions.prediction).count() / predictions.count()
    
    mlflow.log_metric("accuracy", accuracy)
    mlflow.spark.log_model(model, "model")
    
    print(f"✓ Model trained: {accuracy:.2%} accuracy")
    print(f"✓ Run ID: {mlflow.active_run().info.run_id}")

print("✓ Test complete - PostgreSQL + Spark working!")
spark.stop()
