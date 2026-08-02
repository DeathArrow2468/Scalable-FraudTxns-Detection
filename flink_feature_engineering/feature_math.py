import math
from typing import Optional

def compute_average(transaction_count: int, running_sum: float) -> float:
    if transaction_count == 0: return 0.0
    return running_sum / transaction_count

def compute_standard_deviation(transaction_count: int, running_sum: float, running_square_sum: float) -> float:
    if transaction_count <= 1: return 0.0

    mean = compute_average(transaction_count, running_sum)
    variance = (running_square_sum / transaction_count) - (mean * mean)

    return math.sqrt(max(variance, 0.0))

def compute_velocity(recent_transaction_count: int) -> int:
    return recent_transaction_count

def compute_receiver_diversity(unique_receivers: int) -> int:
    return unique_receivers

def compute_receiver_frequency(receiver_frequency: int) -> int:
    return receiver_frequency

def compute_transaction_ratio(transaction_frequency: int, total_transactions: int) -> float:
    if total_transactions == 0: return 0.0
    return transaction_frequency / total_transactions

def compute_balance_difference(old_balance: float, new_balance: float) -> float:
    return old_balance - new_balance

def compute_receiver_balance_difference(old_balance: float, new_balance: float) -> float:
    return new_balance - old_balance

def compute_amount_vs_average(amount: float, average_amount: float) -> float:
    if average_amount == 0: return 0.0
    return amount / average_amount

def compute_amount_vs_previous(amount: float, previous_amount: Optional[float]) -> float:
    if previous_amount is None or previous_amount == 0: return 0.0
    return amount / previous_amount