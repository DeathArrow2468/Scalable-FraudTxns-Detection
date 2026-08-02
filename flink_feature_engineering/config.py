###### Config for Flink Pipeline
AWS_REGION = 'ap-south-1'
INPUT_STREAM = 'fraud-txns'
MAX_HISTORY = 100
FEATURE_VERSION = '1.0.0'
RECENT_WINDOW_MS = 5 * 60 * 1000  # T mins in ms