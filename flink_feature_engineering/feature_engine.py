####### Flink part that takes the income does the relavent updates to sender and receiver
####### and makes the feature vector
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.typeinfo import Types

from flink_feature_engineering.user_profile import UserProfile
from flink_feature_engineering.feature_builder import FeatureBuilder
#from train_dataset_maker.jsonl_writer import JsonlWriter


class FeatureEngine(KeyedProcessFunction):

    def open(self, runtime_context: RuntimeContext):
        descriptor = ValueStateDescriptor(  # descriptor is used to tell flink what the state name and type is
            "user_profile_state",  # name of storage state
            Types.PICKLED_BYTE_ARRAY()  # Since user profile has Deques, classes, optional objs thus, we use this
            # it allows pyflink to pickle and unpickle as it likes
        )

        self.profile_state = runtime_context.get_state(descriptor)
        #self.writer = JsonlWriter("training_vectors.jsonl")

        print("FeatureEngine opened.")

    def process_element(self, transaction, ctx: "KeyedProcessFunction.Context"):

        try:
            profile = self.profile_state.value()  # Feteches a user's details can be None if 1st time user

            ######### ONLY FOR TESTING REMOVE IN PROD ########
            print("Current profile type:", type(profile))
            ##################################################

            if profile is None:
                profile = UserProfile.empty()
                print("Created new UserProfile")

            print("Updating profile...")
            profile.update(transaction)

            print("Building feature vector...")
            feature_vector = FeatureBuilder.build(profile, transaction)

            #print("Writing feature vector...")
            #self.writer.write(feature_vector)

            print("Updating Flink state...")
            self.profile_state.update(profile)

            print("Yielding feature vector...")
            yield feature_vector

        except Exception as e:
            print("ERROR INSIDE process_element():", e)
            raise

    def close(self):
        print("Closing FeatureEngine...")
        #self.writer.close()