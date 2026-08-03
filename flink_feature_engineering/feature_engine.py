####### Flink part that takes the income does the relavent updates to sender and receiver
####### and makes the feature vector
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.typeinfo import Types
from user_profile import UserProfile
from feature_builder import FeatureBuilder
from train_dataset_maker.jsonl_writer import JsonlWriter

class FeatureEngine(KeyedProcessFunction):
    def open(self, runtime_context: RuntimeContext):
        descriptor = ValueStateDescriptor( # descriptor is used to tell flink what the state name and type is
            "user_profile_state", # name of storage state
            Types.PICKLED_BYTE_ARRAY()  # Since user profile has Deques, classes, optional objs thus, we use this
            # it allows pyflink to pickle and unpickle as it likes
        )
        self.profile_state = runtime_context.get_state(descriptor)
        self.writer = JsonlWriter("training_vectors.jsonl")

    def process_element(self, transaction, ctx: "KeyedProcessFunction.Context"):
        profile = self.profile_state.value() # Feteches a user's details can be None if 1st time user

        ######### ONLY FOR TESTING REMOVE IN PROD ########
        print(type(profile))
        ##################################################

        if profile is None:
            profile = UserProfile.empty()

        profile.update(transaction)
        feature_vector = FeatureBuilder.build(profile, transaction)

        self.writer.write(feature_vector)
        self.profile_state.update(profile)

        yield feature_vector

    def close(self):
        self.writer.close()