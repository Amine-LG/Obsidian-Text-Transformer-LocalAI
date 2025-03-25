# Model and Temperature Configuration
MODEL = 'gemma3:4b' # The name of the language model to use (Default: Gemma 3 4B)
TEMPERATURE = 0.0 # The temperature value for controlling randomness in the model's output

# API URL
MODEL_API_URL = 'http://localhost:11434/api/chat' # The URL of the API endpoint for Ollama

# Extended Context Configuration
NUM_CTX = 16384            # Context size for handling larger inputs 

# Keep-Alive Duration
#   "1h" -> keep alive for 1 hour
KEEP_ALIVE = "10m" # The duration for which the model should be kept alive

# Streaming Option
STREAM = True              # Set to True to enable streaming responses, False otherwise

# TIMEOUT sets the maximum time (in seconds) to wait for a response from the server.
# For large requests, we recommend a timeout of at least 2 minutes (e.g., 120 seconds).
TIMEOUT = 120

# Configuration
MAX_FILE_SIZE = 20000 # The maximum file size (in bytes) for processing
MIN_FILE_SIZE = 10 # The minimum file size (in bytes) for processing

# File and Directory Paths
DIRECTORY_PATH = r'D:\Files\Notes\root' # The directory containing the input files

OUTPUT_FOLDER = r'D:\Files\Notes\Obsidian_Enhanced' # The directory where the processed output files will be saved
#  **********************************************************
#  WARNING:  RUNNING THIS SCRIPT WILL DELETE THE OUTPUT FOLDER!
#  ********************************************************** 


# Log File Configuration
LOG_DIRECTORY = 'logs' # The directory where log files will be stored
PROCESS_LOG_FILE = 'process_log.txt' # The name of the file for logging processing details
ERROR_LOG_FILE = 'process_errors_log.txt' # The name of the file for logging errors

# Prompt Configuration
PROMPTS_CONFIG_FILE = 'prompts_config.json' # The name of the JSON file containing the prompts configuration