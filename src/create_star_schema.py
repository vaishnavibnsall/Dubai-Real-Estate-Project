import pandas as pd
import os

# Load cleaned data
df = pd.read_csv("data/cleaned_housing.csv")

# Create folder for star schema files
os.makedirs("data/star_schema", exist_ok=True)

# -------------------------
# 1. PROPERTY DIMENSION
# -------------------------
dim_property = df[
    ["property_type", "furnishing", "completion_status"]
].drop_duplicates().reset_index(drop=True)

dim_property.insert(0, "property_id", range(1, len(dim_property) + 1))


# -------------------------
# 2. LOCATION DIMENSION
# -------------------------
dim_location = df[
    ["country", "city", "address"]
].drop_duplicates().reset_index(drop=True)

dim_location.insert(0, "location_id", range(1, len(dim_location) + 1))


# -------------------------
# 3. PROJECT DIMENSION
# -------------------------
dim_project = df[
    ["project_name"]
].drop_duplicates().reset_index(drop=True)

dim_project.insert(0, "project_id", range(1, len(dim_project) + 1))


# -------------------------
# 4. CONNECT IDs TO FACT TABLE
# -------------------------

df = df.merge(
    dim_property,
    on=["property_type", "furnishing", "completion_status"],
    how="left"
)

df = df.merge(
    dim_location,
    on=["country", "city", "address"],
    how="left"
)

df = df.merge(
    dim_project,
    on=["project_name"],
    how="left"
)


# -------------------------
# 5. FACT TABLE
# -------------------------

fact_property = df[
    [
        "property_id",
        "location_id",
        "project_id",
        "price",
        "bedroom",
        "bathroom",
        "area_sqft",
        "purpose",
        "handover"
    ]
].copy()

fact_property.insert(
    0,
    "property_fact_id",
    range(1, len(fact_property) + 1)
)


# -------------------------
# 6. SAVE EVERYTHING
# -------------------------

dim_property.to_csv(
    "data/star_schema/dim_property.csv",
    index=False
)

dim_location.to_csv(
    "data/star_schema/dim_location.csv",
    index=False
)

dim_project.to_csv(
    "data/star_schema/dim_project.csv",
    index=False
)

fact_property.to_csv(
    "data/star_schema/fact_property.csv",
    index=False
)


# -------------------------
# 7. PRINT RESULTS
# -------------------------

print("STAR SCHEMA CREATED!")
print()

print("dim_property:", dim_property.shape)
print("dim_location:", dim_location.shape)
print("dim_project:", dim_project.shape)
print("fact_property:", fact_property.shape)

print()
print("Files saved inside: data/star_schema/")

print("\n--- FACT TABLE SAMPLE ---")
print(fact_property.head())

print("\n--- PROPERTY DIMENSION SAMPLE ---")
print(dim_property.head())

print("\n--- LOCATION DIMENSION SAMPLE ---")
print(dim_location.head())

print("\n--- PROJECT DIMENSION SAMPLE ---")
print(dim_project.head())

print(os.path.abspath("data/star_schema/dim_property.csv"))