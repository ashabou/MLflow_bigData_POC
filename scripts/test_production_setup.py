#!/usr/bin/env python3
"""Test MLflow with PostgreSQL backend + HDFS artifacts"""

import os
import mlflow
import tempfile
import pyarrow.hdfs


print("=" * 60)
print("Testing MLflow Production Setup")
print("=" * 60)

# Configure MLflow
tracking_uri = "postgresql://mlflow_user:strongpassword@localhost/mlflow_db"
mlflow.set_tracking_uri(tracking_uri)
print("\n✓ Tracking URI set:", tracking_uri)

# Create experiment with HDFS artifact location
experiment_name = "production-test"
artifact_location = "hdfs://localhost:9000/mlflow-artifacts/production-test"

try:
    experiment_id = mlflow.create_experiment(experiment_name, artifact_location=artifact_location)
    print("✓ Created experiment:", experiment_name)
except Exception as e:
    if "already exists" in str(e):
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        print("✓ Using existing experiment:", experiment_name)
    else:
        print("✗ Error creating experiment:", e)
        raise

mlflow.set_experiment(experiment_name)

# Create a test run
print("\n--- Starting Test Run ---")
with mlflow.start_run(run_name="postgresql_hdfs_test"):
    mlflow.log_param("backend", "postgresql")
    mlflow.log_param("artifacts", "hdfs")
    mlflow.log_metric("test_metric", 0.95)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("MLflow Production Setup Test\n")
        test_file = f.name

    print("✓ Logging artifact to HDFS...")
    mlflow.log_artifact(test_file, "test_artifacts")
    os.remove(test_file)
    
    run_id = mlflow.active_run().info.run_id
    print("✓ Run completed! Run ID:", run_id)

print("\n--- Verifying HDFS Storage ---")
os.system("hdfs dfs -ls -R /mlflow-artifacts/production-test 2>/dev/null | head -20")
print("\n✅ Test Complete!")
