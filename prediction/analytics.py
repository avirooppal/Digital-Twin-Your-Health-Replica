import pandas as pd
import numpy as np

# Load the dataset
file_path = "lung_cancer_data.csv"
print(f"📂 Loading dataset from: {file_path}")
df = pd.read_csv(file_path)

# Display the first few rows to inspect the data
print("\n🔍 Preview of the dataset:")
print(df.head())

# Get basic info about the dataset: column types, non-null counts, memory usage, etc.
print("\nℹ️ Dataset Information:")
print(df.info())

# Summary statistics for numerical columns (count, mean, std, min, max, etc.)
print("\n📊 Summary Statistics of Numerical Columns:")
print(df.describe())


