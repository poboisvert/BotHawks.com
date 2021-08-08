# BotHawks- Automated Trading for CoinBase

<img src="https://github.com/poboisvert/BotHawks.com/raw/main/logo.jpg" height="400">

### Folder Cassandra

- Project_Template.ipynb - Performs ETL
- event_data - CSV files to be pre-processed
- event_data_etl.csv - Streamlined file to create database from

### Folder AWS

### Venv

- python3 -m venv env

- source env/bin/activate

- pip freeze > requirements.txt (To generate a txt)

- pip install -r requirements.txt

#### Aiflow

- export AIRFLOW_HOME=~/airflow # Root user
- export AIRFLOW_HOME=$PWD/airflow # Folder application

- pip install apache-airflow

- airflow db init

- airflow webserver -p 8080

- airflow scheduler
