# What is this project?

In this project an ETL pipeline, to process raw data from ANP website was developed. The raw data is about gas stations operation (prices, locations, etc).

- The extract part (E) downloads all the raw data (.csv and .zip files) from the ANP website;
- The transform part (T) applies some transformations to raw data to select useful columns, cast some data types, and create new information;
- The load part (L) loads the transformed data to a data warehouse.

With the data saved in the data warehouse a dashboard, built with Grafana, was developed to monitor some of the aspects of the gas stations operations.

# What is ANP?

ANP is an acronym for Agência Nacional do Petróleo, Gás Natural e Biocombustíveis do Brasil, a Brasilian governamental agency that monitors petrol related topics.

You can find the ANP website [here](https://www.gov.br/anp/pt-br).

# Which files are downloaded?

The folder /catalog has a tables.json file with all routes to use for download data.

You can add more routes if you want. The structure of the .json file is the following:

```
{
    "2022_01": {
        "path": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/precos-semestrais-ca.zip",
        "name": "sh_2022_01.csv"
    },
    "2021_02": {
        "path": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2021-02.csv",
        "name": "sh_2021_02.csv"
    }
}
```

# Which technologies are used?


The framework selected to make the ETL was PySpark.

A data quality check was done with Great Expectations.

A PostgreSQL is used as data warehouse with pgAdmin as a monitor tool.

The dashboard was done with Grafana (it is connected to the data warehouse).

# Data quality checks

After the download of the raw data a Great Expectations pipeline runs to check the data quality. The checks verifies the presence of null values, missing columns, values range, etc.

You can find all the checks in the *expectations.py* file and you can learn more about this module in the oficial documentation [here](https://greatexpectations.io/).

After every download file, a validation runs and saves the results to a .html page which shows all passed (and non passed) checks. You can find this file in the folder validation/data_docs/index.html.

Above, a screenshot of the data quality docs is shown:

This is the first screen:

![GE_1](/static/GE_1.png)

An example of the validation screen:

![GE_2](/static/GE_2.png)


# Dashboard

The dashboard was built with Grafana, reading the data saved in the data warehouse.

All the graphs were ploted using a query which runs with the saved data. You can inspect the queries after running the Grafana service.

The following screenshot shows the dashboard developed:

![GRF](/static/GRF.png)

The /dasboard folder has three files:

- dashboard.yml: a configuration file with the dashboard path;
- datasource.yml: the data warehouse connection file;
- report.json: the dashboard developed (exported from Grafana).

You can read more about this [here](https://grafana.com/docs/grafana/latest/datasources/).

# Environmental variables

A .env file is inside the repository with the environmental variables used by the project. You can change them if you want.

# Data warehouse

A start script is used to create the tables in the data warehouse. This script is copied to the /docker-entrypoint-initdb.d folder to run when the PostgreSQL container starts.

In the folder */database* you can check for the startup script and for the database creation script, that creates two tables:

- ANP: with all the data about the gas stations;
- GAS_STATIONS: only with the most recent data received for each gas station.

The schemas are shown below:

```
CREATE TABLE IF NOT EXISTS ANP (
  "Regiao - Sigla" TEXT,
  "Estado - Sigla" TEXT,
  "Municipio" TEXT,
  "Revenda" TEXT,
  "CNPJ da Revenda" TEXT,
  "Nome da Rua" TEXT,
  "Numero Rua" TEXT,
  "Complemento" TEXT,
  "Bairro" TEXT,
  "Cep" TEXT,
  "Bandeira" TEXT,
  "Produto" TEXT,
  "Unidade de Medida" TEXT,
  "Data da Coleta" DATE,
  "Valor de Compra" DOUBLE PRECISION,
  "Valor de Venda" DOUBLE PRECISION,
  "Valor de Venda Anterior" DOUBLE PRECISION,
  "Data da Coleta Anterior" DATE,
  "Dias entre Coletas" INTEGER
);
```

```
CREATE TABLE IF NOT EXISTS GAS_STATIONS (
  "Regiao - Sigla" TEXT,
  "Estado - Sigla" TEXT,
  "Municipio" TEXT,
  "Revenda" TEXT,
  "CNPJ da Revenda" TEXT,
  "Nome da Rua" TEXT,
  "Numero Rua" TEXT,
  "Complemento" TEXT,
  "Bairro" TEXT,
  "Cep" TEXT,
  "Bandeira" TEXT
);
```

# How to use?

You need to install Docker on your machine to run this project.

After the instalation, you can run the following command:

```
docker compose up
```

To setup the data warehouse (a PostgreSQL), the pgAdmin (to monitor the PostgreSQL), Grafana and the ETL application.

All services are connected in the same network and can communicate with each other.

This code will download all the raw data from the ANP website, runs a data validation step with Great Expectations, make the transformations and loads the data in the data warehouse.

The login and password to connect to the PostgreSQL database are:

```
- PostgreSQL login: postgres
- PostgreSQL password: anp_data_warehouse
```

The database runs in the **5432** port.

To make the connection with Grafana you need to use the following credentials:

```
- Grafana login: anp
- Grafana password: anp
```

The Grafana dashboard is accessible at http://localhost:3000/.

To run the ETL pipeline, outside a docker container, you need to run the following code:

```
poetry run start-pipeline
```

# Folder structure

```
├── Dockerfile.application 
├── Dockerfile.dashboard
├── Dockerfile.database
├── README.md
├── anp_etl
│   ├── __init__.py
│   ├── catalog
│   │   └── tables.json \\ File with paths to download the tables
│   ├── download.py
│   ├── expectations.py \\ File with the GE expectations
│   ├── extract.py      \\ Extract (E) functions
│   ├── load.py         \\ File with load functions
│   ├── shared.py      
│   ├── transform.py    \\ Transform (T) functions
│   └── validation.py   \\ GE functions
├── dashboard
│   ├── dashboard.yml   \\ Grafana instructions to load the saved dashboard
│   ├── datasource.yml  \\ Grafana data souce
│   └── report.json     \\ Grafana saved dashboard
├── data
│   ├── bronze
│   ├── gold
│   │   ├── anp
│   │   └── gas_stations
│   └── silver
│       └── anp_raw
├── database
│   ├── database.sql   \\ Database init (with code to create empty tables)
│   └── setup.sh       \\ File to setup the databse when the container starts
├── docker-compose.yml
├── jars
│   └── postgresql-42.5.1.jar
├── main.py            \\ Main file
├── poetry.lock
├── pyproject.toml
├── static
├── tests
│   ├── __init__.py
│   └── test_anp_pipeline.py
└── validation        \\ Folder used by GE to save the validation data
    ├── checkpoints
    ├── data_docs
    │   └── local_site \\ GE validation site
    ├── expectations
    ├── profilers
```


# TODO

The next step is to run all the pipeline inside an orchestration tool like Apache Airflow.