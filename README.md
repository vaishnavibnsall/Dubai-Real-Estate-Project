# Dubai Real Estate Data Warehouse & ETL Pipeline

A data engineering portfolio project that transforms a messy Dubai real-estate dataset into a structured **SQL data warehouse** using Python, PostgreSQL, and a star schema.

## 🎯 Project Overview

The project takes a raw UAE real-estate dataset and processes it through an ETL pipeline:

**Raw CSV → Data Cleaning → Star Schema → PostgreSQL Database → SQL Analysis**

The goal is to demonstrate practical skills in:

* Python & Pandas
* Data Cleaning
* ETL
* SQL
* Data Modeling
* PostgreSQL
* Data Analysis

## 🛠️ Tech Stack

| Technology   | Purpose                          |
| ------------ | -------------------------------- |
| Python       | Data cleaning and transformation |
| Pandas       | Data processing                  |
| PostgreSQL   | Data warehouse                   |
| Supabase     | Hosted PostgreSQL database       |
| SQL          | Data analysis                    |
| Git & GitHub | Version control                  |

## 🔄 ETL Pipeline

### 1. Extract

A publicly available Dubai real-estate CSV dataset is used as the raw data source.

### 2. Transform

Python and Pandas are used to:

* Clean column names
* Convert numeric fields
* Handle malformed values
* Remove invalid records
* Check missing values
* Check duplicates
* Standardize the dataset

The original dataset contained **5,380 records**.

After cleaning and validation, **3,438 valid property records** remained.

### 3. Load

The cleaned data was transformed into a **star schema** and loaded into a hosted PostgreSQL database using Supabase.

## ⭐ Star Schema

The database consists of one central fact table and three dimension tables:

```text
                 dim_property
                      |
                      |
dim_location ---- fact_property ---- dim_project
                      |
                      |
              Property Measures
        price | bedrooms | bathrooms
              | area | handover
```

### Dimension Tables

**dim_property**

* property_id
* property_type
* furnishing
* completion_status

**dim_location**

* location_id
* country
* city
* address

**dim_project**

* project_id
* project_name

### Fact Table

**fact_property**

* property_fact_id
* property_id
* location_id
* project_id
* price
* bedroom
* bathroom
* area_sqft
* purpose
* handover

## 📊 Data Analysis

SQL queries were created to analyze:

* Property count and average price by property type
* Minimum and maximum prices
* Top locations by number of listings
* Top projects by number of listings
* Average price per square foot
* Furnished vs. unfurnished properties
* Ready vs. off-plan properties

## 📁 Project Structure

```text
dubai-real-estate-project/
│
├── data/
│   ├── raw/                  # Original dataset (not committed)
│   ├── cleaned_housing.csv   # Cleaned dataset (not committed)
│   └── star_schema/          # Generated schema CSVs (not committed)
│
├── notebooks/                # Data exploration notebooks
│
├── src/
│   ├── clean_data.py
│   ├── explore_data.py
│   └── create_star_schema.py
│
├── sql/
│   └── analysis.sql
│
├── dashboard/                # Dashboard files
│
├── .gitignore
└── README.md
```

## 🔒 Dataset & Security

The original dataset and generated CSV files are intentionally excluded from GitHub using `.gitignore`.

This keeps the repository lightweight while allowing the complete ETL process to be reproduced locally.

Database credentials and other secrets should never be committed to GitHub.

## 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/vaishnavibnsall/Dubai-Real-Estate-Project.git
```

Install the required Python libraries:

```bash
pip install pandas
```

Place the original dataset in:

```text
data/raw/uae-housing_dataset.csv
```

Run the ETL scripts:

```bash
python src/clean_data.py
python src/explore_data.py
python src/create_star_schema.py
```

The resulting star-schema CSV files can then be loaded into PostgreSQL/Supabase.

## 📌 Project Status

* [x] Dataset collected
* [x] Data exploration
* [x] Data cleaning
* [x] Star schema design
* [x] PostgreSQL database created
* [x] Data loaded into Supabase
* [x] SQL analysis completed
* [ ] Dashboard
* [ ] Final project documentation

## 👩‍💻 Author

**Vaishnavi Bansal**

Computer Science Student | Data & Technology Projects
