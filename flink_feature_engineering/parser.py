###### Converts incoming json to our txn object
import json
from models import Transaction

def parse_transaction(raw_json: str) -> Transaction:
    data = json.loads(raw_json)

    return Transaction(
        event_number = int(data["event_nnumber"]),
        step = int(data["step"]),
        txn_id = data["txn_id"],

        type = data["type"],
        amount = float(data["amount"]),

        nameOrig = data["nameOrig"],
        nameDest = data["nameDest"],

        oldbalanceOrg = float(data["oldbalanceOrg"]),
        newbalanceOrig = float(data["newbalanceOrig"]),

        oldbalanceDest = float(data["oldbalanceDest"]),
        newbalanceDest = float(data["newbalanceDest"]),

        timestamp = int(data["timestamp"]),
    )