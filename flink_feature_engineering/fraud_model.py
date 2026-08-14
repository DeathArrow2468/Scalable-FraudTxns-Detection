import pandas as pd
import xgboost as xgb

from pyflink.datastream.functions import MapFunction


MODEL_PATH = (
    "/home/ec2-user/Scalable-FraudTxns-Detection/"
    "train_dataset_maker/models/xgboost/Version3/v3.json"
)

FRAUD_THRESHOLD = 0.93

TYPE_MAP = {
    "CASH_IN": 0,
    "CASH_OUT": 1,
    "DEBIT": 2,
    "PAYMENT": 3,
    "TRANSFER": 4
}

FEATURES = [
    "type",
    "amount",
    "velocity",
    "avg_amount",
    "max_amount",
    "min_amount",
    "std_amount",
    "receiver_frequency",
    "receiver_diversity",
    "transfer_ratio",
    "payment_ratio",
    "cashout_ratio",
    "debit_ratio",
    "balance_difference",
    "receiver_balance_difference",
    "amount_vs_average",
    "current_vs_previous",
    "step",
    "amount_y",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest"
]


class FraudModel(MapFunction):

    def open(self, runtime_context):
        self.booster = xgb.Booster()
        self.booster.load_model(MODEL_PATH)

        print(
            f"Fraud model loaded | "
            f"Features={self.booster.num_features()} | "
            f"Threshold={FRAUD_THRESHOLD}"
        )

    def map(self, feature_vector):

        model_input = [[
            TYPE_MAP[feature_vector.type],
            feature_vector.amount,
            feature_vector.velocity,
            feature_vector.avg_amount,
            feature_vector.max_amount,
            feature_vector.min_amount,
            feature_vector.std_amount,
            feature_vector.receiver_frequency,
            feature_vector.receiver_diversity,
            feature_vector.transfer_ratio,
            feature_vector.payment_ratio,
            feature_vector.cashout_ratio,
            feature_vector.debit_ratio,
            feature_vector.balance_difference,
            feature_vector.receiver_balance_difference,
            feature_vector.amount_vs_average,
            feature_vector.current_vs_previous,
            feature_vector.step,
            feature_vector.amount,
            feature_vector.oldbalanceOrg,
            feature_vector.newbalanceOrig,
            feature_vector.oldbalanceDest,
            feature_vector.newbalanceDest
        ]]

        X = pd.DataFrame(model_input, columns=FEATURES)

        score = float(
            self.booster.predict(xgb.DMatrix(X))[0]
        )

        is_fraud = score >= FRAUD_THRESHOLD

        print(
            f"TXN={feature_vector.txn_id} | "
            f"score={score:.6f} | "
            f"decision={'FRAUD' if is_fraud else 'NON-FRAUD'}"
        )

        return feature_vector.txn_id, score, is_fraud