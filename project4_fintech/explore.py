import pandas as pd

credit = pd.read_csv("data/credit/creditcard.csv")

print("=== CREDIT ===")
print(f"Shape: {credit.shape}")
print(credit.head(3))
print(credit.dtypes)
print(credit.isnull().sum().sum())
print(credit['Class'].value_counts())
print(credit['Class'].value_counts(normalize=True) *100)
