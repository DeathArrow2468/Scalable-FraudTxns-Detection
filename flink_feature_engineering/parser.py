import json
from flink_feature_engineering.models import Transaction

def parse_transaction(raw_json):

    print("=" * 80)
    print("TYPE:", type(raw_json))
    print("RAW :", repr(raw_json))
    print("=" * 80)

    if isinstance(raw_json, bytes):
        raw_json = raw_json.decode("utf-8")

    data = json.loads(raw_json)

    return Transaction(
        event_number=int(data["event_number"]),
        step=int(data["step"]),
        txn_id=data["txn_id"],
        type=data["type"],
        amount=float(data["amount"]),
        nameOrig=data["nameOrig"],
        nameDest=data["nameDest"],
        oldbalanceOrg=float(data["oldbalanceOrg"]),
        newbalanceOrig=float(data["newbalanceOrig"]),
        oldbalanceDest=float(data["oldbalanceDest"]),
        newbalanceDest=float(data["newbalanceDest"]),
        timestamp=int(data["timestamp"]),
    )