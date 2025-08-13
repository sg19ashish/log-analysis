## This updated script processes the log files in batches of 10, and each batch is saved into a separate CSV file with incremented numbers.
## This is for reading log files and generating multiple csv files. Use another script to scan and generate one report.

import os
import csv
import re

def extract_log_info(log_line):
    # Regular expression to match the date and cs-uri-stem parts
    match = re.search(r'^(?P<date>\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}.*?\s+(?P<cs_uri_stem>/[^ ]+)', log_line)
    if match:
        date = match.group('date')
        cs_uri_stem = match.group('cs_uri_stem')
        uri_parts = cs_uri_stem.split('/')
        # Extracting the first three parts of the cs-uri-stem
        first_three_parts = '/'.join(uri_parts[:3])  # Including the initial slash
        return date, first_three_parts
    return None, None

def process_log_files(log_dir, output_csv_pattern):
    log_files = os.listdir(log_dir)
    total_files = len(log_files)
    batch_size = 10
    num_batches = (total_files + batch_size - 1) // batch_size  # Calculate the number of batches needed

    for batch_num in range(num_batches):
        batch_files = log_files[batch_num * batch_size : (batch_num + 1) * batch_size]
        output_csv = output_csv_pattern.format(batch_num + 1)
        
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Date', 'First Three Parts of cs-uri-stem'])
            
            for log_filename in batch_files:
                log_path = os.path.join(log_dir, log_filename)
                
                with open(log_path, 'r', encoding='utf-8') as log_file:
                    for line in log_file:
                        date, first_three_parts = extract_log_info(line)
                        if date and first_three_parts:
                            writer.writerow([date, first_three_parts])

# Directory containing log files (use double backslashes or raw string)
log_directory = r'E:\log\log'

# Output CSV file pattern (use double backslashes or raw string)
output_csv_pattern = r'E:\log\log\file_{}.csv'

process_log_files(log_directory, output_csv_pattern)
