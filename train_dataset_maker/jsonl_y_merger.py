import pandas as pd

PATH_CSV = r"C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\paysim_shuffled.csv"
PATH_JSONL = r"C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\train_dataset_maker\train_data\training_vectors.jsonl"

OUTPUT_PATH = r"C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\training_dataset.csv"

# Read engineered features
jsonl = pd.read_json(PATH_JSONL, lines=True)

# Read only the rows we actually have feature vectors for
csv = pd.read_csv(PATH_CSV, nrows=len(jsonl))

# Recreate the producer's event numbers
csv["event_number"] = range(1, len(csv) + 1)

# Merge
merged = jsonl.merge(
    csv,
    on="event_number",
    how="inner"
)

print(f"Feature vectors : {len(jsonl)}")
print(f"CSV rows        : {len(csv)}")
print(f"Merged rows     : {len(merged)}")

assert len(merged) == len(jsonl)
assert merged["event_number"].is_unique

merged.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved successfully to:\n{OUTPUT_PATH}")

print((merged["type_x"] != merged["type_y"]).sum())

print((merged["amount_x"] != merged["amount_y"]).sum())