import os
import shutil
import logging
from tabulate import tabulate
import time
from config import (
    MAX_FILE_SIZE,
    MIN_FILE_SIZE,
    LOG_DIRECTORY,
    PROCESS_LOG_FILE,
    ERROR_LOG_FILE
)

def setup_logging(output_folder):
    """Setup logging configuration and prepare directories."""
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    process_log_path = os.path.join(LOG_DIRECTORY, PROCESS_LOG_FILE)
    error_log_path = os.path.join(LOG_DIRECTORY, ERROR_LOG_FILE)

    # Clear logs and delete output folder at the beginning of each run
    with open(process_log_path, 'w'), open(error_log_path, 'w'):
        pass  # Just opening in 'w' mode clears the files
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Set up logging for errors
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(error_log_path)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    error_logger.addHandler(error_handler)

    # Set up logging for processing details
    process_logger = logging.getLogger('process_logger')
    process_logger.setLevel(logging.INFO)
    process_handler = logging.FileHandler(process_log_path)
    process_handler.setFormatter(logging.Formatter('%(message)s'))
    process_logger.addHandler(process_handler)

    return process_logger, error_logger

def is_text_file(file_path):
    """Check if the file is a typical text file based on its extension."""
    return file_path.lower().endswith(('.txt', '.md'))

def read_files_in_directory(directory_path):
    """
    Read all text files in a directory and categorize them based on size.
    Returns tuples of (file_path, file_size) instead of individual values.

    Note: When files are read using the read_file function (defined elsewhere),
    non-UTF characters will be ignored to prevent decoding errors.
    """
    eligible_files = []
    non_eligible_files = []
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_text_file(file_path):
                file_size = os.path.getsize(file_path)
                if MIN_FILE_SIZE <= file_size <= MAX_FILE_SIZE:
                    eligible_files.append((file_path, file_size))
                else:
                    non_eligible_files.append((file_path, file_size))
    return eligible_files, non_eligible_files

def read_file(file_path):
    """
    Read and return the content of a file, ignoring undecodable characters.
    This is to ensure that the script handles files with any encoding errors by
    skipping undecodable UTF-8 characters.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Failed to read {file_path}: {str(e)}")
        return None

def save_processed_content(output_folder, relative_path, content):
    """Save processed content to the output folder, ensuring .md extension."""
    output_file_path = os.path.join(output_folder, relative_path)
    output_file_path = os.path.splitext(output_file_path)[0] + ".md"
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

def log_processing_details(details, process_logger, total_time):
    """Log the processing details to the process log file."""
    process_logger.info("\n" + tabulate(details, headers="keys", tablefmt="grid"))
    process_logger.info(f"\nTotal Processing Time: {total_time:.1f} seconds")

def display_files_info(eligible_files, non_eligible_files, directory_path):
    """Display information about eligible and non-eligible files."""
    def _display_file_info(files, category_name):
        if files:
            print(f"\n{category_name} Files:")
            data = [
                (
                    os.path.basename(file_path), 
                    file_size, 
                    os.path.relpath(file_path, directory_path)
                ) 
                for file_path, file_size in files
            ]
            print(tabulate(data, headers=["File Name", "Size (bytes)", "Relative Path"], tablefmt="grid"))
        else:
            print(f"\nNo {category_name.lower()} files found.")
    
    _display_file_info(eligible_files, "Eligible")
    _display_file_info(non_eligible_files, "Non-Eligible (exceeding max size or below min size)")

    print(f"\nTotal number of eligible files: {len(eligible_files)}")
    print(f"Total number of non-eligible files: {len(non_eligible_files)}")

def confirm_proceed():
    """Confirm whether to proceed with processing eligible files."""
    proceed = input("Press Enter to proceed with processing eligible files or 'n' to cancel: ").strip().lower()
    return proceed != 'n'

def process_files(processor, eligible_files, output_folder, process_logger, error_logger, directory_path): 
    """Process the eligible files using the specified processor."""
    processing_details = []
    for file_path, file_size in eligible_files:
        try:
            relative_path = os.path.relpath(file_path, directory_path)
            print(f"\nProcessing file: {os.path.basename(file_path)}\n")
            file_content = read_file(file_path)
            
            if file_content is None:
                continue

            start_time = time.time()
            final_content = processor.run(file_content, relative_path)
            processing_time = round(time.time() - start_time, 1)
            
            save_processed_content(output_folder, relative_path, final_content)

            processing_details.append({
                "File Name": os.path.basename(file_path),
                "Size (bytes)": file_size,
                "Processing Time (s)": f"{processing_time:.1f}"
            })

            print("\nFinal Content:\n", final_content)
        except Exception as e:
            error_logger.error(f"Error processing file {file_path}: {e}")
            return processing_details, True 
    return processing_details, False
