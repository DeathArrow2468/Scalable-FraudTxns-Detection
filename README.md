<p align="center">
<img width="600" height="862" alt="image" src="https://github.com/user-attachments/assets/3844ad10-ee32-4911-a18a-67e476281bd8" />
</p>
# **FraudTxnsPipeline**

Real-time fraud detection with AI-assisted enrichment, built on AWS.

FraudTxnsPipeline is an event-driven system for classifying transactions in real time and explaining the ones that look fraudulent. It combines Apache Flink, Amazon Kinesis, SQS, Lambda, PostgreSQL, and Bedrock into a pipeline where the fast decision (fraud or not) and the slow one (why, and what to do about it) never block each other.

**Status**: working end-to-end prototype. Streaming, ML classification, fraud/normal routing, RAG enrichment, and WebSocket delivery are all implemented and running. Each stage is built to be scaled or swapped out on its own.

## How a transaction moves through the system

Everything starts on Kinesis and passes through a Flink job running on EC2, which makes the fraud/not-fraud call using a trained ML model. That's the only part of the pipeline that has to be fast, so it's the only part in the hot path.

From there, Flink routes the transaction to one of two SQS queues based on the classification. Normal transactions go straight to a Lambda that forwards them to a client over WebSocket. Flagged transactions take a longer path: a Lambda pulls context from PostgreSQL, sends it to Bedrock, and produces an enriched explanation of why the transaction looks suspicious. That result lands on its own SQS queue before a WebSocket Lambda delivers it to the client.

Kinesis feeds Flink, Flink decides and routes, SQS absorbs the wait on either side, Lambda does the actual work, and API Gateway pushes the result out over a WebSocket.

## Why it's split up this way

The alternative was one service that ingests, scores, enriches, and delivers everything in one place. That's simpler to write and much worse to run. A slow database query or a Bedrock call that takes 3 seconds instead of 300ms backs up the entire stream, including the transactions that don't need any of that.

Splitting it lets each piece fail or slow down without taking the others with it. The RAG enrichment Lambda can be down for five minutes and fraud events will just sit in the queue until it's back — the streaming job never notices. Same on the delivery side: if a client's WebSocket connection drops, that's a delivery problem, not a fraud-detection problem.

| Component | Job |
|---|---|
| EC2 (Txn Producer) | Generates and publishes transaction events |
| Kinesis | Durable ingestion stream |
| EC2 + Flink | Stateful stream processing, ML classification |
| SQS (Fraud / Normal) | Buffers each path independently |
| Fraud Lambda | RAG enrichment — pulls context, calls Bedrock |
| Normal Lambda | Forwards cleared transactions |
| SQS (RAG-Enriched) | Buffers enriched fraud results before delivery |
| WebSocket Lambdas | Push results to the client |
| PostgreSQL | Context store for enrichment |
| Bedrock | LLM inference for the fraud explanation |
| API Gateway | Client-facing WebSocket endpoint |
| S3 / CloudWatch / VPC | Storage, logs, network isolation |

## Stateful processing in Flink

Fraud detection gets a lot better once you stop treating each transaction as an isolated event. A single large purchase might be nothing, or it might be the fourth unusual transaction from the same account in ten minutes. You only know the difference if something's tracking what came before.

That's what Flink is for here. It holds state keyed by transaction identity (account, device, whatever's relevant) instead of scoring each event blind. Kinesis supplies the durable stream, Flink owns the state, and everything downstream stays stateless. As state size and throughput grow, Flink checkpointing and savepoints are the natural next step for fault recovery, and none of that touches the Lambda layer.

## Delivery guarantees

This pipeline is at-least-once, not exactly-once, unless a specific consumer does the extra work to dedupe. Kinesis and SQS give you durable, asynchronous handoffs, and the tradeoff is that consumers need to tolerate retries and occasional duplicate delivery. That's a more honest description of what actually happens across Kinesis, SQS, Lambda, Postgres, Bedrock, and the WebSocket layer than pretending it's exactly-once end to end.

## ML decides, RAG explains

Two different kinds of intelligence are doing two different jobs here. The Flink job runs a real-time ML model to make the fraud call — fast, cheap, no LLM involved, because every transaction goes through it. Only flagged transactions go further: a Lambda pulls relevant history from PostgreSQL, hands it to Bedrock, and comes back with an explanation instead of just a label. RAG never sits in the critical path. It's an enrichment step that runs after the decision's already made, not a dependency of it.

## Scaling and failure isolation

Because each stage is decoupled, they don't all have to scale together. Kinesis handles ingestion volume through partitioning, Flink adds parallelism as throughput grows, and neither of those changes has to touch the RAG or WebSocket layers.

SQS is what makes that possible. A slow Bedrock call or a database hiccup gets absorbed by the queue instead of propagating upstream. If the RAG Lambda goes down entirely, fraud events pile up in the queue and get processed once it's back, while the Flink job keeps running the whole time. The same isolation applies to delivery: a client disconnecting or a WebSocket Lambda misbehaving has no effect on fraud detection upstream.

This matters most when transaction volume, LLM latency, and client connectivity are all unpredictable at the same time, which in practice is most of the time.

## Security and observability

VPC handles network isolation, IAM scopes permissions per component, CloudWatch covers logs and metrics, and API Gateway is the one client-facing surface. For an actual production deployment, the next additions would be Secrets Manager, encryption at rest, private subnets, tighter security groups, dead-letter queues, and infrastructure as code. None of that changes the architecture, it just hardens it.

## Repository layout

```
producer/   transaction generation
flink/      ingestion, state/feature processing, ML inference, routing
lambda/     fraud RAG enrichment, normal consumer, WebSocket delivery
rag/        retrieval, context construction, Bedrock calls
database/   PostgreSQL schema and integration
client/     real-time display
```

Directory names can change. What matters is that the boundaries between them — events and queues — stay explicit, since that's what keeps each piece independently testable and replaceable.

## What's working, what's next

**Implemented**: Kinesis ingestion, Flink stream processing, ML classification, independent fraud/normal queues, RAG enrichment through Bedrock and PostgreSQL, WebSocket delivery through API Gateway, full VPC deployment. Both the normal and fraud paths run end to end.

**Next**: Flink checkpointing/savepoints, dead-letter queues and retry policies, idempotency keys for downstream writes, horizontal Flink scaling, Secrets Manager, infrastructure as code, load testing, and metrics for end-to-end latency, queue depth, and model performance. All of these extend the current design. None of them require rearchitecting it.

## Stack

- **Streaming**: Apache Flink, Amazon Kinesis
- **ML**: Python, running inside the Flink job
- **Messaging**: Amazon SQS
- **Compute**: EC2, Lambda
- **AI/RAG**: Amazon Bedrock, PostgreSQL
- **Storage**: S3
- **Networking**: VPC
- **Delivery**: API Gateway + WebSockets
- **Observability**: CloudWatch
