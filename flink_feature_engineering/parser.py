from flink_feature_engineering.models import Transaction

def parse_transaction(raw):
    if isinstance(raw, bytes): raw = raw.decode("utf-8")
    raw = raw.strip("{}")
    data = {}

    for item in raw.split(","):
        k, v = item.split(":", 1)
        data[k.strip()] = v.strip()

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