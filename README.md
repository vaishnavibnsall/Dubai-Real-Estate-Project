# Dubai Real Estate Data Warehouse & ETL Pipeline

A beginner-friendly portfolio project using a real, messy Dubai real-estate CSV.

## Current status

Only the project structure is set up. No data has been created, cleaned, modeled, or inserted into a database yet.

## Project structure

```text
dubai-real-estate-project/
├── data/
│   ├── raw/          # Put the original CSV here
│   └── processed/    # Cleaned data will be created here later
├── notebooks/        # Optional pandas exploration notebooks
├── src/              # Python ETL code will go here later
├── sql/              # Schema, load, and useful query code later
├── dashboard/        # Dashboard application later
└── .gitignore
```

## Next step

1. Put your **real source CSV** in `data/raw/`.
2. Keep the original file unchanged so you can always trace your work back to the source.
3. Tell me the CSV filename. I will inspect its actual header and a few sample rows first.
4. After that, we will create a short data-quality checklist. We will not choose fact or dimension columns until we have seen the real column names.

## Rules for this project

- Do not create fake data.
- Do not guess column names.
- Clean the data step by step with pandas.
- Make small commits after each completed stage.
- Keep secrets such as database passwords in `.env`, never in code or GitHub.
