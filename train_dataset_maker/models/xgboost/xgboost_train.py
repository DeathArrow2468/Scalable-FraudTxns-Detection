import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

PATH = r"C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\train_dataset_maker\train_data\training_dataset.csv"
SAVE_PATH = r'C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\train_dataset_maker\train_data\models\xgboost\Version3\v3.json'
THRESHOLD = 0.93  # Play around to figure out the best, 0.93 seems to be pretty good


df = pd.read_csv(PATH)
print(df.columns)
df = df.drop(columns=["txn_id", "event_number", "isFlaggedFraud", "nameOrig", "nameDest", "type_y"])
# We drop type_y cause its always equal to type_x
df = df.rename(columns={"type_x":"type", "amount_x":"amount"})
ls = LabelEncoder()
df["type"] = ls.fit_transform(df["type"])
### Analysis on the distribution of the dataset
print(df["isFraud"].value_counts())
print(df["isFraud"].value_counts(normalize=True))

print(f"Dataframe shape: {df.shape}")
################################################

X = df.drop(columns=['isFraud'])
Y = df['isFraud']

### Datatype check
print(f"Data types in X: {X.dtypes}")
print(f"Data type in Y: {Y.dtypes}")

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42)

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42, stratify=y_train)

### Done to inform xgboost about the dataset imbalance
negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

scale_pos_weight = negative / positive

model = xgb.XGBClassifier(n_estimators=100,  # Max number of trees
                          subsample=0.8, # Number of random samples used to train a trss
                          early_stopping_rounds=50, # Number of rounds after which training stops if no improv
                          eval_metric=["aucpr","auc"],  # Cause the dataset is very imbalanced, used to measure performance
                          max_depth=6,  # Max depth of a tree
                          learning_rate=0.05, # Shrinks the contribution of a new tree before adding it to the ensemble of trees
                          random_state=42,
                          reg_alpha=0.1, # L1 regularization i.e to encourage sparse trees i.e reduces the splits in the tree
                          # Makes small leaf weight's zero making that split useless which is thus, avoided my the model thereafter
                          reg_lambda=1, # L2 regularization i.e used to prevent large leaf weights
                          # Leaf weights are the final output from a tree, they contribute to the overall score from multiple trees, this sum is 
                          # raw_score that get sigmoided to get a probability
                          tree_method='hist', # Histogram way of training to reduce runtime, little loss in acc
                          # rather than splitting on every possible row value it groups the values in bins and splits based on them
                          objective="binary:logistic", # Tells the model we're trying to predict a probability
                          scale_pos_weight=scale_pos_weight # Tell the model to focus on the fraud samples more when training
                          )

model.fit(x_train, y_train,
          verbose=10, # Print performance every 10 boosting rounds
          eval_set=[(x_val, y_val)],  # Using only validation set to deceide early stopping
          )

pred = model.predict_proba(x_test)[:,1] # Not .predict cause then the threshold is 0.5 we need to play with the threshold
# i.e it stores the actual predicted values
# [:, 1] cause we get probabilites as (notFraud, isFraud) so we take the 2nd column i.e 1 and use that for eval and preds
pred = (pred >= THRESHOLD).astype(int) # Final binary classification, 1 is Fraud, 0 is NOT_Fraud

### Gives precision, recall, f1
print(classification_report(y_test, pred))

### Save model
model.save_model(SAVE_PATH)

### Confusion Matrix
cm = confusion_matrix(y_test, pred)
display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
display.plot(cmap=plt.cm.Blues)
plt.show()

### Shows most useful parameters being used
xgb.plot_importance(model, max_num_features=20) # Top x parameters
plt.show()



