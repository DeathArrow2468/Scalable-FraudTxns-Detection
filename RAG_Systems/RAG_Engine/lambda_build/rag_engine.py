from config import *
from search import SearchEngine
from utils.titan_embedder import TitanEmbedder
from utils.llm import BedrockLLM

class RAGEngine:
    def __init__(self):
        self.embedder = TitanEmbedder()
        self.search_engine = SearchEngine()
        self.llm = BedrockLLM()

    def retrieve(self, query):
        embedding = self.embedder.embed(query)

        research = self.search_engine.vector_search(
            RETRIEVER_1_TABLE, embedding, TOP_K_RESEARCH
        )

        guideline = self.search_engine.vector_search(
            RETRIEVER_3_TABLE, embedding, TOP_K_GUIDELINES
        )

        return research, guideline

    def close(self):
        self.search_engine.close()


    def build_context(self, research, guidelines):
        context = "RESEARCH:\n\n"
        for result in research:
            context += f"""
            Score: {result.score}
            {result.text}
            """

        context += "GUIDELINES:\n\n"

        for result in guidelines:
            context += f"""
            Score: {result.score}
            {result.text}
            """

        return context

    def build_prompt(self, query, context):
        return f"""
            You are a bank fraud detection research assistant.

            Answer the user's question using the provided research
            and regulatory/guideline context.

            The query is a set of various feature vectors that describe the metadata
            of the transaction each term is defined in the form of a comma seperated table as follows:

            "feature","type","description","formula_or_computation"
            "txn_id","string","Unique transaction identifier (UUID).","-"
            "event_number","int","Sequential order of events for this account (starts at 1).","-"
            "type","categorical","Transaction type: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER.","-"
            "amount","float","Monetary value of the transaction (local currency).","-"
            "vel","int","Count of transactions for the same user_id in the last 5 min (sliding window).","vel = count(transactions in last 5 min)"
            "avg_amount","float","Mean transaction amount for the user over the same 5-min window.","avg = sum(amount) / vel"
            "max_amount","float","Maximum amount seen in the 5-min window.","max = max(amount)"
            "min_amount","float","Minimum amount seen in the 5-min window.","min = min(amount)"
            "std_amount","float","Standard deviation of amounts in the 5-min window (0 if vel <= 1).","std = sqrt(sum((amount - avg)^2) / vel)"
            "receiver_frequency","int","How many times the current nameDest (receiver) has appeared as a receiver for this user in the last 5 min.","Count of distinct events where nameDest repeats in last 5 min"
            "receiver_diversity","int","Number of unique receivers the user has sent to in the last 5 min.","count(distinct nameDest in last 5 min)"
            "transfer_ratio","float","Fraction of user's 5-min volume that is TRANSFER type.","sum(amount where type=TRANSFER) / sum(amount)"
            "payment_ratio","float","Fraction of volume that is PAYMENT type.","sum(amount where type=PAYMENT) / sum(amount)"
            "cashout_ratio","float","Fraction of volume that is CASH_OUT type.","sum(amount where type=CASH_OUT) / sum(amount)"
            "debit_ratio","float","Fraction of volume that is DEBIT type.","sum(amount where type=DEBIT) / sum(amount)"
            "balance_difference","float","Change in the sender's account balance caused by this txn (negative = money out).","newBalanceOrig - oldBalanceOrig"
            "receiver_balance_difference","float","Change in the receiver's account balance caused by this txn.","newBalanceDest - oldBalanceDest"
            "amount_vs_average","float","Ratio of current amount to the user's 5-min avg_amount (1 = exactly average).","amount / avg_amount"
            "current_vs_previous","float","Ratio of current amount to the immediately previous transaction amount for the same user (1 = same size).","amount_t / amount_{{t-1}} (if no previous, set to 1)"

            User question:
            {query}

            Retrieved context:
            {context}

            Provide a clear and evidence-based answer.
            """.strip()

    def answer(self, query):
        research, guidelines = self.retrieve(query)

        context = self.build_context(research, guidelines)
        prompt = self.build_prompt(query, context)

        return self.llm.generate(prompt)

    
if __name__ == "__main__":
    engine = RAGEngine()
    try:
        ans = engine.answer("How can account takeover fraud be detected?")
    except Exception as e:
        print(f"Error in main rag_engine: {e}")
        raise

    print(ans)

    