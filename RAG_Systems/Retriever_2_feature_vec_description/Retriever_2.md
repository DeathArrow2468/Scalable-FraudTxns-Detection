
### Feature Descriptions & Formulas

| Feature                         | Type        | Description                                                                                                            | Formula / Computation                                  |
| ------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `txn_id`                      | string      | Unique transaction identifier (UUID).                                                                                  | –                                                     |
| `event_number`                | int         | Sequential order of events for this account (starts at 1).                                                             | –                                                     |
| `type`                        | categorical | Transaction type:`CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER`.                                      | –                                                     |
| `amount`                      | float       | Monetary value of the transaction (local currency).                                                                    | –                                                     |
| `vel` (velocity)              | int         | Count of transactions for the same`user_id` in the last 5 min (sliding window).                                    | `vel =                                                 |
| `avg_amount`                  | float       | Mean transaction amount for the user over the same 5‑min window.                                                      | `avg = (�� amount) / vel`                          |
| `max_amount`                  | float       | Maximum amount seen in the 5‑min window.                                                                              | `max = max(amount)`                                  |
| `min_amount`                  | float       | Minimum amount seen in the 5‑min window.                                                                              | `min = min(amount)`                                  |
| `std_amount` (σ)             | float       | Standard deviation of amounts in the 5‑min window (0 if`vel≤1`).                                                   | `σ = sqrt( (��(amount−avg)²) / vel )`           |
| `receiver_frequency`          | int         | How many times the current`nameDest` (receiver) has appeared as a receiver for this user in the last 5 min.        | Count of distinct events where`nameDest` repeats     |
| `receiver_diversity`          | int         | Number of**unique** receivers the user has sent to in the last 5 min.                                          | `                                                      |
| `transfer_ratio`              | float       | Fraction of user’s 5‑min volume that is`TRANSFER` type.                                                            | `��_{type=TRANSFER} amount / �� amount`          |
| `payment_ratio`               | float       | Fraction of volume that is`PAYMENT` type.                                                                            | `��_{type=PAYMENT} amount / �� amount`           |
| `cashout_ratio`               | float       | Fraction of volume that is`CASH_OUT` type.                                                                           | `��_{type=CASH_OUT} amount / �� amount`          |
| `debit_ratio`                 | float       | Fraction of volume that is`DEBIT` type.                                                                              | `��_{type=DEBIT} amount / �� amount`             |
| `balance_difference`          | float       | Change in the sender’s account balance caused by this txn (negative = money out).                                     | `newBalanceOrig − oldBalanceOrig`                   |
| `receiver_balance_difference` | float       | Change in the receiver’s account balance caused by this txn.                                                          | `newBalanceDest − oldBalanceDest`                   |
| `amount_vs_average`           | float       | Ratio of current`amount` to the user’s 5‑min `avg_amount` (1 = exactly average).                                 | `amount / avg_amount`                                |
| `current_vs_previous`         | float       | Ratio of current`amount` to the **immediately previous** transaction amount for the same user (1 = same size). | `amount_t / amount_{t-1}` (if no previous, set to 1) |
