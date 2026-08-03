########## Main file used to start flink and all its processes
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kinesis import FlinkKinesisConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types

from flink_feature_engineering.config import INPUT_STREAM
from flink_feature_engineering.parser import parse_transaction
from flink_feature_engineering.feature_engine import FeatureEngine

def main():
    env = StreamExecutionEnvironment.get_execution_environment()    # Flink runtime
    env.set_parallelism(1) # env is where everything occurs, (x) x is the number of CPUs you are using
    #### It's set to one cause there is only one shard of incomeing data froom Kinesis

    consumer = FlinkKinesisConsumer(    # Makes the connection to kinesis
        INPUT_STREAM,   # Stream name
        SimpleStringSchema(),   # Kinesis stores in bytes we want it in string
        {}  # EC2 credentials when left empty it'll default to the attached role
    )

    ds = env.add_source(consumer) # data stream, this is the point where the kinesis stream is taken in

    transactions = ds.map(  # Converts the string to tranaction class's format
        parse_transaction, # function to convert
        output_type=Types.PICKLED_BYTE_ARRAY()  # Datatype for Flink to know what it is
    )
    #####################################
    # Btw, we use Types.PICKED_BYTE_ARRAY() cause there isn't a pre-dined datatype in
    # flink for Transaction class it is our own class afterall!
    # This does create some overhead which is feasible for our scale of project which is
    # ~100 transactions/sec but for higher order we should make a custom serializer
    #####################################
    features = (transactions
                .key_by(lambda txn: txn.nameOrig)   # Allows flink to route a txn to a profile it's like a hashmap's hash
                .process(FeatureEngine()) # Every tranaction is now sent to Feature Engine where updates, feature vector building etc. happen
                )

    ####### For debugging/training remove in PROD! ###########
    features.print()
    #################################################

    # The above is jus the building of pipeline
    env.execute("Real-Time Scalable Fraud Feature Engineering") # Calls actual exection of pipeline

if __name__ == "__main__":
    main()