import pandas as pd
PATH = 'paysim.csv'

df = pd.read_csv(PATH)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('paysim_shuffled.csv', index=False)

