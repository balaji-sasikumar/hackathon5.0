import os
import csv
import json

def get_csv_headers(directory):
    headers_map = {}
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return headers_map

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    # Read the first row (header)
                    try:
                        header = next(reader)
                        headers_map[filename] = header
                    except StopIteration:
                        # Empty file
                        headers_map[filename] = []
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return headers_map

if __name__ == "__main__":
    data_folder = "Hack-Data"
    # Ensure we are looking in the correct relative path if running from project root
    # The user's workspace root seems to be /Users/balaji/Documents/Projects/POC/hackathon5.0
    # and Hack-Data is inside it.
    
    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, data_folder)
    
    # Fallback if script is run from a different location but Hack-Data is relative to script
    if not os.path.exists(target_dir):
         script_dir = os.path.dirname(os.path.abspath(__file__))
         target_dir = os.path.join(script_dir, data_folder)

    result = get_csv_headers(target_dir)
    print(result)
    
    # Write result to JSON file
    json_output_path = os.path.join(current_dir, 'headers.json')
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
    print(f"Headers exported to {json_output_path}")
