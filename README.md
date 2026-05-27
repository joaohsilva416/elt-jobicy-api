# ELT Jobicy API

## About

Extract remote job listings from the Jobicy API, load them into Snowflake, and transform the raw data using dbt. The goal is to build a clean, analytics-ready dataset of remote job opportunities with salary information.

## Tech Stack

- **Python**: Main programming language
- **Requests**: Library for HTTP requests
- **Pandas**: Library for data manipulation
- **SQLAlchemy + snowflake-sqlalchemy**: Libraries to connect to Snowflake
- **python-dotenv**: Library to manage environment variables
- **Snowflake**: Cloud data warehouse to store the collected data
- **dbt**: Data transformation framework (silver layer)
- **Jobicy API**: Remote job listings data source

## Environment Set-up

**1. Install dependencies:**

If you don't have Poetry installed, follow the [official documentation](https://python-poetry.org/docs/).

```bash
poetry install
```

**2. Set up the environment variables**

Create a `.env` file in the project root and add the following variables:

```env
ACCOUNT=snowflake_account
USER=username
PASSWORD=password
DATABASE=database_name
SCHEMA=schema_name
WAREHOUSE=warehouse_name
```

**3. Configure the dbt profile**

Create or update `~/.dbt/profiles.yml` with your Snowflake connection:

```yaml
elt_jobicy_api:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('ACCOUNT') }}"
      user: "{{ env_var('USER') }}"
      password: "{{ env_var('PASSWORD') }}"
      database: "{{ env_var('DATABASE') }}"
      schema: "{{ env_var('SCHEMA') }}"
      warehouse: "{{ env_var('WAREHOUSE') }}"
```

**4. Snowflake**

Make sure your Snowflake account is configured and accessible with the credentials above.

## How to Run

**1. Clone the repository**

```bash
git clone git@github.com:<your-user>/elt-jobicy-api.git
```

**2. Navigate to the project folder**

```bash
cd elt-jobicy-api
```

**3. Run the extraction and load pipeline**

```bash
poetry run python src/jobicy_api.py
```

**4. Run the dbt transformation**

```bash
cd elt_jobicy_api
poetry run dbt run
```
