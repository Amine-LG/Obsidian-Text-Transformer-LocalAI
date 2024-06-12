import time
from tabulate import tabulate
from prompt_processor import PromptProcessor
import file_utils
from config import (
    DIRECTORY_PATH, 
    OUTPUT_FOLDER,
    PROMPTS_CONFIG_FILE
)

def main():
    process_logger, error_logger = file_utils.setup_logging(OUTPUT_FOLDER)
    
    processor = PromptProcessor(OUTPUT_FOLDER)
    processor.load_prompts_from_json(PROMPTS_CONFIG_FILE)

    eligible_files, non_eligible_files = file_utils.read_files_in_directory(DIRECTORY_PATH)
    
    if not eligible_files and not non_eligible_files:
        print("No suitable text files found in the specified directory.")
        return
    
    print(f"Original Directory Path: {DIRECTORY_PATH}\n")

    file_utils.display_files_info(eligible_files, non_eligible_files, DIRECTORY_PATH)

    if not file_utils.confirm_proceed():
        print("Processing cancelled.")
        return

    total_start_time = time.time()

    processing_details, error_occurred = file_utils.process_files(processor, eligible_files, OUTPUT_FOLDER, process_logger, error_logger, DIRECTORY_PATH) 

    total_processing_time = round(time.time() - total_start_time, 1)

    if processing_details:
        print("\nProcessing Summary:")
        print(tabulate(processing_details, headers="keys", tablefmt="grid"))
    else:
        print("No files were processed.")

    file_utils.log_processing_details(processing_details, process_logger, total_processing_time)

    print(f"\nTotal Processing Time: {total_processing_time} seconds")

    if not error_occurred:
        print("Processing completed successfully!")
    else:
        print("Processing completed with errors. Please check the error log for details.")

if __name__ == "__main__":
    main()
