######## Builds and returns a Feature vector that is ready to be fed to a ML model
######## Function calls for compute to keep the code clean
from flink_feature_engineering.models import Transaction, FeatureVector
from flink_feature_engineering.user_profile import UserProfile

from flink_feature_engineering.feature_math import (
    compute_average,
    compute_standard_deviation,
    compute_velocity,
    compute_receiver_diversity,
    compute_receiver_frequency,
    compute_transaction_ratio,
    compute_balance_difference,
    compute_receiver_balance_difference,
    compute_amount_vs_average,
    compute_amount_vs_previous
)

class FeatureBuilder:
    @staticmethod
    def build(profile: UserProfile, transaction: Transaction) -> FeatureVector:
        stats = profile.running_statistics
        receiver_stats = profile.receiver_statistics
        txn_stats = profile.transaction_statistics
        last_txn = profile.last_transaction

        avg_amount = compute_average(stats.transaction_count,
                                    stats.running_sum
                                    )

        num_transactions = stats.transaction_count

        return FeatureVector(
            txn_id = transaction.txn_id,
            event_number = transaction.event_number,

            amount = transaction.amount,
            type = transaction.type,

            avg_amount = avg_amount,
            velocity = compute_velocity(len(profile.recent_transactions)),
            max_amount = stats.max_amount,
            min_amount = stats.min_amount,

            std_amount = compute_standard_deviation(
                stats.transaction_count,
                stats.running_sum,
                stats.running_square_sum
            ),

            receiver_frequency = compute_receiver_frequency(receiver_stats.frequency(transaction.nameDest)),

            receiver_diversity = compute_receiver_diversity(receiver_stats.diversity()),

            transfer_ratio = compute_transaction_ratio(txn_stats.transaction_frequency.get("TRANSFER", 0), 
                                                    num_transactions),

            payment_ratio = compute_transaction_ratio(txn_stats.transaction_frequency.get("PAYMENT", 0), 
                                                            num_transactions),

            cashout_ratio = compute_transaction_ratio(txn_stats.transaction_frequency.get("CASH_OUT", 0), 
                                                            num_transactions),

            debit_ratio = compute_transaction_ratio(txn_stats.transaction_frequency.get("DEBIT", 0), 
                                                            num_transactions),

            balance_difference = compute_balance_difference(transaction.oldbalanceOrg, transaction.newbalanceOrig),

            receiver_balance_difference = compute_receiver_balance_difference(transaction.oldbalanceDest, transaction.newbalanceDest),

            amount_vs_average = compute_amount_vs_average(transaction.amount, avg_amount),

            current_vs_previous = compute_amount_vs_previous(transaction.amount, None if last_txn is None else last_txn.amount),

            # Raw fields required by XGBoost
            step=transaction.step,
            oldbalanceOrg=transaction.oldbalanceOrg,
            newbalanceOrig=transaction.newbalanceOrig,
            oldbalanceDest=transaction.oldbalanceDest,
            newbalanceDest=transaction.newbalanceDest
        )


        
        