### This takes the CSV files once generated from first script and counts the number of times value has been repeated and captures it in a csv file.
## It also excludes the keywords from the first column. Use it to remove noise

import os
import csv
from collections import Counter

# List of keywords to exclude
excluded_keywords = [
    '.well-known', '.git', '.env', '_vti_bin', '.cobalt', '_images', '_pages',
    '?.jsp', '.tar.gz', '.tgz', '.gzip', '.zip', '_vti_inf.html', '_wpeprivate',
    '.hg', '~bin', '.htaccess', '.svn', '_ScriptLibrary', '_private', '_vti_cnf', '_vti_bot', 'vti_log', 'vti_pvt', 'vti_script', 'vti_txt', 
    '_vti_shm', 'apple-touch', 'actuator', '/admin/', 'administrator', 'Archive', 'favicon.ico', '_api', 'backup', 'default', '/debug/',
    '/docker-compose.yml', '/database.sql', '/db.sql', '/conf', '/aspnet_client/', 'cgi', '/assets/', 'php', '/DEADJOE', '/adm-bin/',
    '/adojavas.inc', '/adovbs.inc', '/art/', '/asp/', '/bin', '/cacti', '/css/', '/data', '/demo/', 'dev', 'development', '/doc/', '/docs/',
    'console', '/CHANGELOG.txt', 'config', '/dana-na', 'aspera', '/DocLink', '/createou', 'doesntexist'
    
]

def count_and_split_uri_stem_occurrences(csv_dir):
    uri_stem_counter = Counter()
    split_values = []

    # Iterate through all CSV files in the directory
    for csv_filename in os.listdir(csv_dir):
        if csv_filename.endswith('.csv'):
            csv_path = os.path.join(csv_dir, csv_filename)
            
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                
                for row in reader:
                    uri_stem = row['First Three Parts of cs-uri-stem']
                    
                    # Check if any excluded keyword is in the uri_stem
                    if any(keyword in uri_stem for keyword in excluded_keywords):
                        continue
                    
                    uri_stem_counter[uri_stem] += 1

                    parts = uri_stem.split('/')
                    first_part = parts[1] if len(parts) > 1 else ''
                    second_part = parts[2] if len(parts) > 2 else ''
                    third_part = '/'.join(parts[3:]) if len(parts) > 3 else ''
                    
                    split_values.append((uri_stem, first_part, second_part, third_part))

    return uri_stem_counter, split_values

def write_counts_and_splits_to_csv(counts, splits, output_csv):
    with open(output_csv, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['First Two Parts of cs-uri-stem', 'First Part', 'Second Part', 'Remaining Parts', 'Count'])
        
        for uri_stem, count in counts.items():
            first_part, second_part, third_part = next((x[1], x[2], x[3]) for x in splits if x[0] == uri_stem)
            writer.writerow([uri_stem, first_part, second_part, third_part, count])

# Directory containing CSV files (use double backslashes or raw string)
csv_directory = r'C:\Users\Downloads\TEMP\logs\prod-traffic'

# Output CSV file for counts (use double backslashes or raw string)
output_csv_file = r'C:\Users\Downloads\TEMP\logs\prod-traffic\uri_stem_counts.csv'

# Count occurrences and split URI stems
uri_stem_counts, split_values = count_and_split_uri_stem_occurrences(csv_directory)

# Write counts and splits to output CSV
write_counts_and_splits_to_csv(uri_stem_counts, split_values, output_csv_file)
