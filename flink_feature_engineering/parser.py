import json
import sys
from flink_feature_engineering.models import Transaction

def parse_transaction(raw_json):

    sys.stdout.write("=" * 80 + "\n")
    sys.stdout.write(str(type(raw_json)) + "\n")
    sys.stdout.write(repr(raw_json) + "\n")
    sys.stdout.flush()

    if isinstance(raw_json, bytes):
        raw_json = raw_json.decode("utf-8")

    try:
        data = json.loads(raw_json)
    except Exception:
        print("FAILED JSON:", repr(raw_json), flush=True)
        raise

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