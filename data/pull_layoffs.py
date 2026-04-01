import pandas as pd

df = pd.read_csv("layoffs.csv")

print(df.head(10))
print(df.columns.tolist())

print("\nTotal rows:", len(df))
print("\nLayoffs by industry:")
print(df.groupby("industry")["total_laid_off"].sum().sort_values(ascending=False).head(10))