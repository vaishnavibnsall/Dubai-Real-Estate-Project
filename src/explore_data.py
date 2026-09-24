import pandas as pd

df = pd.read_csv("data/cleaned_housing.csv")

print("\nPROPERTY TYPES:")
print(df["property_type"].value_counts())

print("\nCITIES:")
print(df["city"].value_counts())

print("\nPURPOSE:")
print(df["purpose"].value_counts())

print("\nFURNISHING:")
print(df["furnishing"].value_counts())

print("\nCOMPLETION STATUS:")
print(df["completion_status"].value_counts())

print("\nPROJECTS:")
print(df["project_name"].nunique())

print("\nDUPLICATES:")
print(df.duplicated().sum())