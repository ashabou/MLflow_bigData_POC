import sys
print("Python version:", sys.version)
print()
try:
    import pyspark
    print("✅ PySpark installed:", pyspark.__version__)
except ImportError as e:
    print("❌ PySpark not found:", e)
try:
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("test").master("local[*]").getOrCreate()
    print("✅ Spark session created:", spark.version)
    spark.stop()
except Exception as e:
    print("❌ Spark session failed:", e)
