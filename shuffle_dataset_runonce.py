import pandas as pd
PATH = 'paysim.csv'

pd.read_csv(PATH).sample(frac=1, random_state=42).to_csv('paysim_shuffled.csv')

