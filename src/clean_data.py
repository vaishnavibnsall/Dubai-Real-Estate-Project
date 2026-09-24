import pandas as pd

# 1. Load raw CSV
input_file = "data/raw/uae-housing_dataset.csv"
df = pd.read_csv(input_file)

print("Original shape:", df.shape)


# 2. Clean column names
df = df.rename(columns={
    "propert_type": "property_type",
    "area(sqft)": "area_sqft"
})


# 3. Clean price
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")


# 4. Clean area
df["area_sqft"] = (
    df["area_sqft"]
    .astype(str)
    .str.replace(" sqft", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["area_sqft"] = pd.to_numeric(df["area_sqft"], errors="coerce")


# 5. Clean bedroom
# Extract only the number at the beginning.
# "Studio" becomes 0.
df["bedroom"] = df["bedroom"].astype(str)

df.loc[
    df["bedroom"].str.lower().str.contains("studio"),
    "bedroom"
] = "0"

df["bedroom"] = pd.to_numeric(
    df["bedroom"].str.extract(r"(\d+(?:\.\d+)?)")[0],
    errors="coerce"
)


# 6. Clean bathroom
df["bathroom"] = df["bathroom"].astype(str)

df["bathroom"] = pd.to_numeric(
    df["bathroom"].str.extract(r"(\d+(?:\.\d+)?)")[0],
    errors="coerce"
)


# 7. Remove duplicate rows
df = df.drop_duplicates()


# 8. Remove rows where important numeric data is missing
df = df.dropna(
    subset=["price", "area_sqft", "bedroom", "bathroom"]
)


# 9. Convert bedroom and bathroom to integers
df["bedroom"] = df["bedroom"].astype(int)
df["bathroom"] = df["bathroom"].astype(int)


# 10. Save cleaned dataset
output_file = "data/cleaned_housing.csv"
df.to_csv(output_file, index=False)


# 11. Display results
print("Cleaned shape:", df.shape)

print("\nCleaned columns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 cleaned rows:")
print(df.head())

print("\nCleaned file saved to:", output_file)