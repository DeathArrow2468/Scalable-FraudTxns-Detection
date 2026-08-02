import pandas as pd
PATH = 'paysim.csv'

df = pd.read_csv(PATH)

# num_frauds = 0
# for x in df['isFraud']:
#     if x == 1: 
#         num_frauds = num_frauds + 1

num_frauds = (df['isFraud'] == 1).sum()
print(f"Number of isfraud entries: {num_frauds}")

num_Notfrauds = (df['isFraud'] == 0).sum()
print(f"Number of isfraud entries: {num_Notfrauds}")

num_accounts_sending = df['nameOrig'].nunique()
print(f"Number of unique Sending accounts: {num_accounts_sending}")

num_accounts_reci = df['nameDest'].nunique()
print(f"Number of unique Sending accounts: {num_accounts_reci}")