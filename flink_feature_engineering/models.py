######## Classes to define txns and feature vector which we later
######## feed to the ML model(s)
from dataclasses import dataclass

@dataclass
class Transaction:
    event_number: int
    step: int
    txn_id: str
    type: str
    amount: float
    nameOrig: str
    nameDest: str
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    timestamp: int

@dataclass
class TransactionSummary:
    amount: float
    receiver: str
    transaction_type: str
    timestamp: int
    sender_old_balance: float
    sender_new_balance: float
    receiver_old_balance: float
    receiver_new_balance: float

@dataclass
class FeatureVector:
    # Meta data for LLM+RAG and employee to track txn with
    txn_id: str
    event_number: int

    #Data for ML as well
    type: str
    amount: float

    velocity: int # Number of transactions in recent history
    avg_amount: float
    max_amount: float
    min_amount: float
    std_amount: float

    receiver_frequency: int # NUmber of time money has gone form this acc. to the other specific acc.
    receiver_diversity: int # Number of unique accounts payments go to

    transfer_ratio: float # num transfer txns / tot txn
    payment_ratio: float # num payment txns / tot txn
    cashout_ratio: float # num cashout txns / tot txns
    debit_ratio: float # num debit txns / tot txns

    balance_difference: float
    receiver_balance_difference: float

    amount_vs_average: float # current amount / avg amount
    current_vs_previous: float # current amount / prev mount

    # Raw transaction fields required by v3.json
    step: int
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

