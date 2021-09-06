# BotHawks - Automated Trade Recommendation for CoinBase

The purpose of this project is to simply and provide an easy access to fetch price quotation form the coinbase API.

URL: http://bothawks.com/ | https://bothawks.web.app

## Front End

<img src="https://github.com/poboisvert/BotHawks.com/raw/main/logo.png" height="400">

The client interface offer live price update from the Coinbase API and a possible subscription to alert.

## Back End

### Folder Cassandra

- Project_Template.ipynb - Performs ETL
- event_data - CSV files to be pre-processed
- event_data_etl.csv - Streamlined file to create database from

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

#### MongoDB

> mongo

> show dbs

> use cryptocurrency_database

> db.BTC_collection.find()

> db.dropDatabase()

#### References

- https://github.com/danpaquin/coinbasepro-python
- https://github.com/danielktaylor/PyLimitBook
- https://towardsdatascience.com/moving-averages-in-python-16170e20f6c#:~:text=The%20simple%20moving%20average%20is,at%20the%20expense%20of%20accuracy.&text=The%20easiest%20way%20to%20calculate,is%20by%20using%20the%20pandas.
