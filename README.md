# Install Python 3.10 & venv
```
sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-dev
```

# Install pip & virtualenv
```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
pip install virtualenv
```

# Create Virtual Environment
```
python3.10 -m venv mlflow-env
source mlflow-env/bin/activate
```

# Execute Ansible Playbook
```
ansible-playbook -i inventory2.ini start-all-cluster.yml
```

# Clone repo containing playbooks
```
git clone git@github.com:ashabou/MLflow_bigData_POC.git
cd MLflow_bigData_POC
```

# Check if Pyspark works Correctly
```
pyspark
```

# Ensure Spark uses Python 3.10
```
export PYSPARK_PYTHON=python3.10
export PYSPARK_DRIVER_PYTHON=python3.10
```


# Install required Packages
```
pip install pyarrow psycopg2-binary py4j mlflow scikit-learn matplotlib
```

# Configure PostgreSQL as MLflow Metadata Store
- PostgreSQL Installation (on metadata server node)
```
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

- Create Database & User
```
CREATE DATABASE mlflowdb;
CREATE USER mlflowuser WITH ENCRYPTED PASSWORD 'mlflowpass';
GRANT ALL PRIVILEGES ON DATABASE mlflowdb TO mlflowuser;
```

- Create users, and databases, based on Access rights of Teams
```
[mlflow]
backend-store-uri = postgresql://mlflowuser:mlflowpass@<db_host>:5432/mlflowdb
```

# Configure HDFS for Artifacts
- Ensure HDFS is running
```
hdfs dfs -mkdir -p /mlflow/artifacts
hdfs dfs -chmod -R 777 /mlflow/artifacts
```

- Update config:
```
[mlflow]
backend-store-uri = postgresql://mlflowuser:mlflowpass@<db_host>:5432/mlflowdb
default-artifact-root = hdfs://<namenode_host>:9000/mlflow/artifacts
```

# Start MLflow Tracking Server
```
mlflow server     --backend-store-uri postgresql+psycopg2://mlflow_user:mlflow_password_2025@localhost:5432/mlflow_db     --default-artifact-root ./mlruns     --host 0.0.0.0 --port 5001

```

make sure you have packaging-21.3 : 
```
pip install "packaging<22"
```


