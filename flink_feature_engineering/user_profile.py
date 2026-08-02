from collections import deque
from dataclasses import dataclass, field

from typing import Deque, Dict, Optional

from config import MAX_HISTORY, RECENT_WINDOW_MS
from models import Transaction, TransactionSummary, FeatureVector

@dataclass
class RunningStatistics:
    transaction_count: int = 0
    running_sum: float = 0
    running_square_sum: float = 0
    max_amount: float = field(default_factory=lambda: float("-inf"))
    min_amount: float = field(default_factory=lambda: float("inf"))

    def update(self, amount: float):
        self.transaction_count += 1
        self.running_sum += amount
        self.running_square_sum += amount * amount
        self.max_amount = max(self.max_amount, amount)
        self.min_amount = min(self.min_amount, amount)

@dataclass
class ReceiverStatistics:
    receiver_frequency: Dict[str, int] = field(default_factory = dict)

    def update(self, receiver: str):
        self.receiver_frequency[receiver] = (self.receiver_frequency.get(receiver, 0) + 1)

    def frequency(self, receiver: str) -> int:
        return self.receiver_frequency.get(receiver, 0)

    def diversity(self) -> int:
        return len(self.receiver_frequency)

@dataclass
class TransactionTypeStatistics:
    transaction_frequency: Dict[str, int] = field(default_factory = dict)

    def update(self, transaction_type: str):
        self.transaction_frequency[transaction_type] = (self.transaction_frequency.get(transaction_type, 0) + 1)

    def ratio(self, transaction_type: str, total_transactions: int) -> float:
        if total_transactions == 0: return 0.0

        return (self.transaction_frequency.get(transaction_type, 0) / total_transactions)

@dataclass
class UserProfile:
    recent_transactions: Deque[TransactionSummary] = field(default_factory=deque)
    historical_transactions: Deque[TransactionSummary] = field(default_factory=deque)

    running_statistics: RunningStatistics = field(default_factory=RunningStatistics)
    receiver_statistics: ReceiverStatistics = field(default_factory=ReceiverStatistics)

    transaction_statistics: TransactionTypeStatistics = field(default_factory=TransactionTypeStatistics)
    last_transaction: Optional[TransactionSummary] = None

    def _create_summary(self, transaction: Transaction) -> TransactionSummary:
        return TransactionSummary(
            amount = transaction.amount,
            receiver = transaction.nameDest,
            transaction_type = transaction.type,
            timestamp = transaction.timestamp,
            sender_old_balance = transaction.oldbalanceOrg,
            sender_new_balance = transaction.newbalanceOrig,
            receiver_old_balance = transaction.oldbalanceDest,
            receiver_new_balance = transaction.newbalanceDest
        )

    def _update_historical_transactions(self, summary: TransactionSummary):
        self.historical_transactions.append(summary)
        if len(self.historical_transactions) > MAX_HISTORY:
            self.historical_transactions.popleft()

    def _update_recent_transactions(self, summary: TransactionSummary):
        self.recent_transactions.append(summary)

        cutoff = summary.timestamp - RECENT_WINDOW_MS

        while(self.recent_transactions and self.recent_transactions[0].timestamp < cutoff):
            self.recent_transactions.popleft()

    def update(self, transaction: Transaction):
        summary = self._create_summary(transaction)
        self.running_statistics.update(summary.amount)
        self.receiver_statistics.update(summary.receiver)
        self.transaction_statistics.update(summary.transaction_type)
        self._update_recent_transactions(summary)
        self._update_historical_transactions(summary)
        self.last_transaction = summary

    @classmethod
    def empty(cls): # Allows us to return a new instance of UserProfile class
        return cls()