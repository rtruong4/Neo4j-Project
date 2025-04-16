import os
import glob

data_dir = "./data"

for subfolder in os.listdir(data_dir):
    subfolder_path = os.path.join(data_dir, subfolder)
    
    if os.path.isdir(subfolder_path):
        # Find all JSON files in the subfolder
        json_files = glob.glob(os.path.join(subfolder_path, "*.json"))
        
        for json_file in json_files:
            # Check if 'twitter' is NOT in the filename
            if "twitter" not in os.path.basename(json_file).lower():
                print(f"Deleting: {json_file}")
                os.remove(json_file)